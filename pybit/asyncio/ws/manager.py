import asyncio
import json
import traceback
import logging
import enum
from typing import (
    Optional,
    List
)

from pybit import _helpers
from pybit._http_manager import generate_signature
from pybit._websocket_stream import (
    SUBDOMAIN_MAINNET,
    SUBDOMAIN_TESTNET,
    DOMAIN_MAIN,
    TLD_MAIN,
)
import websockets as ws
from websockets.exceptions import ConnectionClosedError
from websockets_proxy import (
    Proxy,
    proxy_connect
)

from pybit.asyncio.utils import get_event_loop
from pybit.asyncio.ws.utils import get_reconnect_wait


PING_INTERVAL = 20
PINT_TIMEOUT = 10
MESSAGE_TIMEOUT = 5
PRIVATE_AUTH_EXPIRE = 1


logger = logging.getLogger(__name__)


class WSState(enum.Enum):
    INITIALISING = 1
    EXITING = 2
    STREAMING = 3
    RECONNECTING = 4


class AsyncWebsocketManager:
    """
    Implementation of async API for Bybit
    """

    def __init__(
            self,
            channel_type: str,
            url: str,
            subscription_message: List[str],
            testnet: Optional[bool] = False,
            rsa_authentication: Optional[bool] = False,
            api_key: Optional[str] = None,
            api_secret: Optional[str] = None,
            proxy: Optional[str] = None,
            queue: Optional[asyncio.Queue] = None,
            tld: Optional[str] = TLD_MAIN,
    ):
        self.channel_type = channel_type
        self.url = url
        self.subscription_message = subscription_message
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.proxy = proxy
        self.rsa_authentication = rsa_authentication
        self.tld = tld
        self.queue = queue or asyncio.Queue()
        self._loop = get_event_loop()
        self._handle_read_loop = None

        self.ws_state = WSState.INITIALISING
        self.custom_ping_message = json.dumps({"op": "ping"})
        self.ws = None
        self._conn = None
        self._keepalive = None
        self.MAX_RECONNECTS = 60
        self._reconnects = 0
        self.MAX_QUEUE_SIZE = 10000
        self.downtime_callback = None

    async def __aenter__(self) -> "AsyncWebsocketManager":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.ws_state = WSState.EXITING
        if self.ws:
            await self.ws.close()
        if self._conn and hasattr(self._conn, 'protocol'):
            await self._conn.__aexit__(exc_type, exc_val, exc_tb)

    def _handle_message(self, res: str) -> dict:
        return json.loads(res)

    async def _read_loop(self):
        logger.info(f"Start loop.")
        while True:
            try:
                match self.ws_state:
                    case WSState.STREAMING:
                        res = await asyncio.wait_for(self.ws.recv(), timeout=MESSAGE_TIMEOUT)
                        res = self._handle_message(res)
                        if res.get("op") == "pong" or res.get("op") == "ping":
                            continue
                        if res.get("op") == "subscribe":
                            if res.get("success") is not None and res["success"] is False:
                                if res.get("ret_msg") == "Request not authorized":
                                    logger.warning(f"Cancel task because request: {res}")
                                    raise asyncio.CancelledError()
                                logger.error(f"False connecting: {res}")
                                self.ws_state = WSState.RECONNECTING
                            continue

                        if res:
                            await self.queue.put(res)

                    case WSState.EXITING:
                        logger.info("Exiting websocket")
                        await self.ws.close()
                        self._keepalive.cancel()
                        break
                    case WSState.RECONNECTING:
                        while self.ws_state == WSState.RECONNECTING:
                            await self._reconnect()
                    case self.ws.protocol.State.CLOSING:
                        await asyncio.sleep(0.1)
                        continue
                    case self.ws.protocol.State.CLOSED:
                        await self._reconnect()

            except asyncio.TimeoutError:
                continue
            except ConnectionResetError as e:
                logger.warning(f"Received connection reset by peer. Error: {e}. Trying to reconnect.")
                await self._reconnect()
            except asyncio.CancelledError:
                logger.warning("Cancelled Error")
                self._keepalive.cancel()
                break
            except OSError as e:
                logger.warning(f"Os Error: {e}")
                await self._reconnect()
                continue
            except ConnectionClosedError as e:
                logger.warning(f"Connection Closed Error: {e}")
                self._keepalive.cancel()
                await self._reconnect()
                continue
            except Exception as e:
                logger.warning(f"Unknown exception: {e}")
                continue

    async def _auth(self):
        """
        Prepares authentication signature per Bybit API specifications.
        """

        expires = _helpers.generate_timestamp() + (PRIVATE_AUTH_EXPIRE * 1000)
        param_str = f"GET/realtime{expires}"
        signature = generate_signature(
            use_rsa_authentication=self.rsa_authentication,
            secret=self.api_secret,
            param_str=param_str
        )
        # Authenticate with API.
        await self.ws.send(json.dumps({"op": "auth", "args": [self.api_key, expires, signature]}))

    async def _keepalive_task(self):
        try:
            while True:
                await asyncio.sleep(PING_INTERVAL)

                await self.ws.send(self.custom_ping_message)
        except asyncio.CancelledError:
            logger.error(f'Ping cancellation error')
            traceback.print_exc()
            return
        except ConnectionClosedError as e:
            logger.error(f'Ping connection closed error: {e}')
            traceback.print_exc()
            return
        except Exception as e:
            logger.error(f"Keepalive failed")
            traceback.print_exc()
            raise e

    async def _reconnect(self):
        if self.ws_state == WSState.EXITING:
            logger.warning(f"Websocket was closed")
            await self.queue.put({
                "success": False,
                "ret_msg": "Max reconnect reached"
            })
            return

        self.ws_state = WSState.RECONNECTING
        if self._reconnects < self.MAX_RECONNECTS:
            reconnect_wait = get_reconnect_wait(self._reconnects)
            logger.info( f"{self.MAX_RECONNECTS - self._reconnects} left")
            await asyncio.sleep(reconnect_wait)
            self._reconnects += 1
            await self.connect()
            logger.info(f"Reconnected")
        else:
            logger.error("Max reconnections reached")
            await self.queue.put({
                "success": False,
                "ret_msg": "Max reconnect reached"
            })
            self.ws_state = WSState.EXITING

    async def connect(self):
        if self.ws is None or self.ws_state == WSState.RECONNECTING:
            subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
            endpoint = self.url.format(SUBDOMAIN=subdomain, DOMAIN=DOMAIN_MAIN, TLD=self.tld)

            if self.proxy:
                logger.info(f"Connected via: {self.proxy}")
                self._conn = proxy_connect(endpoint,
                                           close_timeout=0.1,
                                           open_timeout=60,
                                           ping_interval=None,
                                           ping_timeout=None,
                                           proxy=Proxy.from_url(self.proxy))
            else:
                logger.info(f"Connected without proxies")
                self._conn = ws.connect(endpoint,
                                        close_timeout=0.1,
                                        open_timeout=60,
                                        ping_timeout=None,  # We use custom ping task
                                        ping_interval=None)
            try:
                self.ws = await self._conn.__aenter__()
            except Exception as e:
                traceback.print_exc()
                await self._reconnect()
                logger.error(f"Connecting error: {e}")
                return
            # Authenticate for private channels
            if self.api_key and self.api_secret:
                await self._auth()

            # subscribe to channels
            for mes in self.subscription_message:
                await self.ws.send(mes)
        self._reconnects = 0
        self.ws_state = WSState.STREAMING
        logger.info(f"Connected successfully")
        if self.downtime_callback is not None:
            try:
                self.downtime_callback()
            except Exception as e:
                logger.error(f"Downtime callback error")
                traceback.print_exc()
        if self._keepalive:
            self._keepalive.cancel()
        self._keepalive = asyncio.create_task(self._keepalive_task())
        if not self._handle_read_loop:
            self._handle_read_loop = self._loop.call_soon_threadsafe(asyncio.create_task, self._read_loop())

    async def close_connection(self):
        self.ws_state = WSState.EXITING

    async def recv(self, timeout: int = 5):
        try:
            return await asyncio.wait_for(self.queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None
