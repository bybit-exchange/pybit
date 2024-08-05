import asyncio
import json
import traceback
import logging
from typing import Optional
from random import random

from pybit import _helpers
from pybit._http_manager._auth import generate_signature
from pybit.exceptions import InvalidWebsocketSubscription
from pybit._websocket_stream import (
    SUBDOMAIN_MAINNET,
    SUBDOMAIN_TESTNET,
    DOMAIN_MAIN
)
from pybit.asyncio.websocket._utils import get_loop
from pybit.asyncio.websocket.enums import WSState
import websockets as ws
from websockets.exceptions import ConnectionClosedError


logger = logging.getLogger(__name__)





PING_INTERVAL = 20
PINT_TIMEOUT = 10
MESSAGE_TIMEOUT = 5
PRIVATE_AUTH_EXPIRE = 1


class AsyncWebsocketManager:
    """
    Implementation of async API for Bybit
    """

    def __init__(self,
                 channel_type: str,
                 url: str,
                 testnet: bool,
                 subscription_message: str,
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None):
        self.channel_type = channel_type
        self.testnet = testnet
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = url
        self.subscription_message = subscription_message
        self.queue = asyncio.Queue()
        self._loop = get_loop()
        self._handle_read_loop = None

        self.ws_state = WSState.INITIALISING
        self.custom_ping_message = json.dumps({"op": "ping"})
        self.ws = None
        self._conn = None
        self._keepalive = None
        self.MAX_RECONNECTS = 5
        self._reconnects = 0
        self.MAX_RECONNECT_SECONDS = 300
        self.MAX_QUEUE_SIZE = 10000

    async def __aenter__(self) -> "AsyncWebsocketManager":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.ws_state = WSState.EXITING
        if self.ws:
            self.ws.fail_connection()
        if self._conn and hasattr(self._conn, 'protocol'):
            await self._conn.__aexit__(exc_type, exc_val, exc_tb)

    def _handle_message(self, res: str) -> dict:
        return json.loads(res)

    async def _read_loop(self):
        logger.info(f"Start loop")

        while True:
            try:
                if self.ws_state == WSState.STREAMING:
                    res = await asyncio.wait_for(self.ws.recv(), timeout=MESSAGE_TIMEOUT)
                    res = self._handle_message(res)
                    # Check if message is pong
                    if res.get("op") == "pong":
                        continue
                    if res.get("op") == "subscribe":
                        if res.get("success", True) is False:
                            logger.error(f"Subscription error: {res}")
                            raise InvalidWebsocketSubscription(response=res)

                    if res:
                        await self.queue.put(res)
                elif self.ws_state == WSState.EXITING:
                    logger.info("_read_loop. Exit websocket")
                    await self.ws.close()
                    self._keepalive.cancel()
                    await asyncio.sleep(0.1)
                    await self.__aexit__(None, None, None)
                    break
                elif self.ws_state == WSState.RECONNECTING:
                    while self.ws_state == WSState.RECONNECTING:
                        await self._reconnect()

            except asyncio.TimeoutError:
                continue
            except ConnectionResetError as e:
                logger.warning(f"Received connection reset by peer. Error: {e}. Trying to reconnect.")
                await self._reconnect()
            except asyncio.CancelledError:
                logger.warning("Cancelled error")
                self._keepalive.cancel()
                break
            except OSError as e:
                traceback.print_exc()
                await self._reconnect()
                continue
            except ConnectionClosedError as e:
                logger.warning("Connection closed")
                await self._reconnect()
                continue
            except Exception as e:
                traceback.print_exc()
                logger.warning(f"Unknown exception: {e}.")
                self.ws_state = WSState.EXITING
                continue

    async def _auth(self):
        """
        Prepares authentication signature per Bybit API specifications.
        """

        expires = _helpers.generate_timestamp() + (PRIVATE_AUTH_EXPIRE * 1000)
        param_str = f"GET/realtime{expires}"
        signature = generate_signature(use_rsa_authentication=False, secret=self.api_secret, param_str=param_str)
        # Authenticate with API.
        await self.ws.send(json.dumps({"op": "auth", "args": [self.api_key, expires, signature]}))

    async def _keepalive_task(self):
        try:
            while True:
                await asyncio.sleep(PING_INTERVAL)

                await self.ws.send(self.custom_ping_message)

        except asyncio.CancelledError:
            return
        except ConnectionClosedError:
            return
        except Exception:
            logger.error(f"Keepalive failed")
            traceback.print_exc()

    async def _reconnect(self):
        if self.ws_state == WSState.EXITING:
            logger.warning(f"Websocket was closed.")
            await self.queue.put({
                "success": False,
                "ret_msg": "Max reconnect reached"
            })
            return

        self.ws_state = WSState.RECONNECTING
        if self._reconnects < self.MAX_RECONNECTS:
            reconnect_wait = self._get_reconnect_wait(self._reconnects)
            logger.info(f"{self.MAX_RECONNECTS - self._reconnects} left")
            await asyncio.sleep(reconnect_wait)
            self._reconnects += 1
            await self.connect()
            logger.info(f"Reconnected. Key: ")
        else:
            logger.error("Max reconnections reached")
            await self.queue.put({
                "success": False,
                "ret_msg": "Max reconnect reached"
            })
            self.ws_state = WSState.EXITING

    def _get_reconnect_wait(self, attempts: int) -> int:
        expo = 2 ** attempts
        return round(random() * min(self.MAX_RECONNECT_SECONDS, expo - 1) + 1)

    async def connect(self):
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        endpoint = self.url.format(SUBDOMAIN=subdomain, DOMAIN=DOMAIN_MAIN)
        self._conn = ws.connect(endpoint,
                                close_timeout=0.1,
                                ping_timeout=None,  # We use custom ping task
                                ping_interval=None)
        try:
            self.ws = await self._conn.__aenter__()
        except Exception as e:
            await self._reconnect()
            traceback.print_exc()
            return
        # Authenticate for private channels
        if self.api_key and self.api_secret:
            await self._auth()

        await self.ws.send(self.subscription_message)
        self._reconnects = 0
        self.ws_state = WSState.STREAMING
        if not self._handle_read_loop:
            self._keepalive = asyncio.create_task(self._keepalive_task())
            logger.info(f"Connected successfully")
            self._handle_read_loop = self._loop.call_soon_threadsafe(asyncio.create_task, self._read_loop())

    async def close_connection(self):
        self.ws_state = WSState.EXITING

    async def recv(self):
        res = None
        while not res:
            if self.ws_state == WSState.EXITING:
                break
            try:
                res = await asyncio.wait_for(self.queue.get(), timeout=MESSAGE_TIMEOUT)
                if not res.get("data"):
                    # Only responses with "data" key contains useful information
                    # Other payloads contains system info
                    continue
            except asyncio.TimeoutError:
                continue
        return res
