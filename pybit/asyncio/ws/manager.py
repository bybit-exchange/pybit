import asyncio
import enum
import json
import logging
import time
from typing import (
    Callable,
    List,
    Optional,
)
from urllib.parse import urlsplit

import websockets as ws
from websockets.exceptions import ConnectionClosed, ConnectionClosedError

from pybit import _helpers
from pybit._http_manager import generate_signature
from pybit._websocket_stream import (
    SUBDOMAIN_MAINNET,
    SUBDOMAIN_TESTNET,
    DEMO_SUBDOMAIN_MAINNET,
    DEMO_SUBDOMAIN_TESTNET,
    DOMAIN_MAIN,
    TLD_MAIN,
)
from pybit.asyncio.ws.utils import get_reconnect_wait


PING_INTERVAL = 20
PING_TIMEOUT = 10
MESSAGE_TIMEOUT = 5
AUTH_ACK_TIMEOUT = 10


logger = logging.getLogger(__name__)


class WSState(enum.Enum):
    INITIALISING = 1
    EXITING = 2
    STREAMING = 3
    RECONNECTING = 4


class AuthFailedError(ConnectionError):
    """Raised when the server rejects the WebSocket auth frame.

    Distinct from generic connection errors so ``connect()`` can bail out
    immediately instead of retrying up to ``MAX_RECONNECTS`` times with
    known-bad credentials (which risks IP-level rate limiting).
    """


def _redact_proxy(proxy: Optional[str]) -> str:
    """Return a proxy string safe for logs.

    Users routinely embed credentials in proxy URLs (http://user:pass@host);
    log aggregators (Datadog/ELK/CloudWatch) will collect any info-level line
    that contains them.
    """
    if not proxy:
        return "<none>"
    try:
        host = urlsplit(proxy).hostname
        return host or "<proxy>"
    except Exception:
        return "<proxy>"


class AsyncWebsocketManager:
    """Async Bybit WebSocket manager (pull model).

    Consumers pull frames off ``.recv()``. Connect/reconnect, keepalive, and
    auth are handled internally.

    Terminal frame contract: when the stream shuts down (max-reconnect,
    auth failure, or explicit user close), exactly one sentinel is enqueued
    carrying ``"type": "terminal"``, a ``"reason"`` code, plus
    ``success`` and ``ret_msg``. Consumers should treat any frame with
    ``type == "terminal"`` as "the stream is done — stop calling recv()".

    ``reason`` values:
      - ``"max_reconnect"``  — connect() exhausted MAX_RECONNECTS.
      - ``"auth_failed"``    — server rejected the auth frame.
      - ``"user_close"``     — application called ``close_connection()``.
    """

    MAX_RECONNECTS = 60
    MAX_QUEUE_SIZE = 10000

    def __init__(
            self,
            channel_type: str,
            url: str,
            subscription_message: List[str],
            testnet: Optional[bool] = False,
            demo: Optional[bool] = False,
            rsa_authentication: Optional[bool] = False,
            api_key: Optional[str] = None,
            api_secret: Optional[str] = None,
            proxy: Optional[str] = None,
            queue: Optional[asyncio.Queue] = None,
            tld: Optional[str] = TLD_MAIN,
            private_auth_expire: int = 1,
            downtime_callback: Optional[Callable] = None,
            queue_maxsize: Optional[int] = None,
    ):
        self.channel_type = channel_type
        self.url = url
        self.subscription_message = subscription_message
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.demo = demo
        self.proxy = proxy
        self.rsa_authentication = rsa_authentication
        self.tld = tld
        self.private_auth_expire = private_auth_expire
        self.downtime_callback = downtime_callback

        self._queue_maxsize = (
            queue_maxsize if queue_maxsize is not None else self.MAX_QUEUE_SIZE
        )
        # ``asyncio.Queue`` binds to the current event loop at construction on
        # Python 3.9 (raises ``RuntimeError`` if none exists yet); build lazily
        # so ``AsyncWebsocketManager`` can be instantiated outside a loop.
        self._queue: Optional[asyncio.Queue] = queue

        self.ws_state = WSState.INITIALISING
        self.custom_ping_message = json.dumps({"op": "ping"})
        self.ws = None
        self._conn = None
        self._keepalive: Optional[asyncio.Task] = None
        self._handle_read_loop: Optional[asyncio.Task] = None
        self._last_pong = 0.0

    @property
    def queue(self) -> asyncio.Queue:
        """Frame queue. Lazily created on first access from within a running loop."""
        if self._queue is None:
            self._queue = asyncio.Queue(maxsize=self._queue_maxsize)
        return self._queue

    async def __aenter__(self) -> "AsyncWebsocketManager":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()

    def _handle_message(self, res: str) -> dict:
        return json.loads(res)

    async def _process_frame(self, frame: dict) -> None:
        """Handle control frames; put stream data on the queue."""
        op = frame.get("op")
        # Bybit v5 sends pong ACKs as ``{"op": "ping", "ret_msg": "pong", ...}``
        # rather than ``op == "pong"``. Recognise both forms — otherwise
        # ``_last_pong`` never advances and the half-open detector fires
        # after 30s, triggering an endless reconnect loop.
        if op == "pong" or frame.get("ret_msg") == "pong":
            self._last_pong = time.monotonic()
            return
        if op == "ping":
            return
        if op == "subscribe":
            if frame.get("success") is False:
                ret_msg = frame.get("ret_msg", "")
                if "not authorized" in ret_msg.lower():
                    # Terminal auth error — surface to consumer instead of
                    # tearing down the read loop with a bare CancelledError.
                    logger.error(f"Subscription rejected (unauthorized): {frame}")
                    await self._enqueue({
                        "success": False,
                        "ret_msg": ret_msg or "Request not authorized",
                        "op": "subscribe",
                    })
                    self.ws_state = WSState.EXITING
                    return
                # Non-auth subscribe failure (e.g. invalid topic): surface to
                # the consumer and keep the socket alive. Triggering a
                # reconnect here would resend the same failing subscription
                # message on every attempt — connect() itself succeeds each
                # cycle, so its MAX_RECONNECTS counter never advances and the
                # loop turns into a tight tear-down/rebuild storm, potentially
                # getting the IP rate-limited or banned.
                logger.error(f"Subscribe error: {frame}")
                await self._enqueue(frame)
            return
        await self._enqueue(frame)

    async def _enqueue(self, item: dict) -> None:
        try:
            self.queue.put_nowait(item)
        except asyncio.QueueFull:
            # Drop-oldest keeps the stream alive rather than blocking the read
            # loop; log so users notice a slow consumer.
            logger.warning("WS queue full — dropping oldest frame")
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            self.queue.put_nowait(item)

    async def _read_loop(self):
        logger.info("Start read loop")
        consecutive_unknown = 0
        while True:
            try:
                state = self.ws_state
                if state == WSState.EXITING:
                    logger.info("Exiting websocket read loop")
                    return
                if state == WSState.RECONNECTING:
                    # Keepalive and _process_frame set RECONNECTING but don't
                    # actually reconnect — driving that here keeps the reconnect
                    # single-tasked (this loop is the only concurrent driver).
                    await self._reconnect()
                    continue
                if state != WSState.STREAMING or self.ws is None:
                    await asyncio.sleep(0.05)
                    continue

                res = await asyncio.wait_for(self.ws.recv(), timeout=MESSAGE_TIMEOUT)
                frame = self._handle_message(res)
                if frame:
                    await self._process_frame(frame)
                consecutive_unknown = 0

            except asyncio.TimeoutError:
                # No data within MESSAGE_TIMEOUT — check half-open TCP by pong staleness.
                if self._is_pong_stale():
                    logger.warning("Pong stale — treating as half-open, reconnecting")
                    self.ws_state = WSState.RECONNECTING
                    await self._reconnect()
                continue
            except asyncio.CancelledError:
                # Cooperative cancellation — propagate.
                logger.info("Read loop cancelled")
                raise
            except (ConnectionClosed, ConnectionClosedError) as e:
                if self.ws_state == WSState.EXITING:
                    return
                logger.warning(f"Connection closed: {e}")
                self.ws_state = WSState.RECONNECTING
                await self._reconnect()
            except ConnectionResetError as e:
                logger.warning(f"Connection reset: {e}. Reconnecting.")
                self.ws_state = WSState.RECONNECTING
                await self._reconnect()
            except OSError as e:
                logger.warning(f"OS error: {e}. Reconnecting.")
                self.ws_state = WSState.RECONNECTING
                await self._reconnect()
            except Exception:
                consecutive_unknown += 1
                logger.exception("Unknown error in read loop")
                # Sleep to prevent hot-loop CPU burn; switch to reconnect if it persists.
                await asyncio.sleep(0.5)
                if consecutive_unknown >= 3:
                    logger.error("Too many unknown errors — reconnecting")
                    self.ws_state = WSState.RECONNECTING
                    await self._reconnect()
                    consecutive_unknown = 0

    def _is_pong_stale(self) -> bool:
        if self._last_pong == 0.0:
            return False
        return (time.monotonic() - self._last_pong) > (PING_INTERVAL + PING_TIMEOUT)

    async def _auth(self):
        """Send auth frame and read the server ACK inline.

        Reading inline (vs. hand-off to the read loop) is required because
        ``_auth`` is called from inside ``connect()`` *before* the read loop
        starts serving frames — the loop only reads while state is STREAMING.
        Delegating the ACK to the loop would deadlock every authenticated
        connect until the ACK read timed out.
        """
        expires = _helpers.generate_timestamp() + (self.private_auth_expire * 1000)
        param_str = f"GET/realtime{expires}"
        signature = generate_signature(
            use_rsa_authentication=self.rsa_authentication,
            secret=self.api_secret,
            param_str=param_str,
        )
        await self.ws.send(json.dumps({
            "op": "auth",
            "args": [self.api_key, expires, signature],
        }))
        try:
            raw = await asyncio.wait_for(self.ws.recv(), timeout=AUTH_ACK_TIMEOUT)
        except asyncio.TimeoutError:
            raise ConnectionError("Auth ACK timed out")
        try:
            frame = json.loads(raw)
        except (ValueError, TypeError) as e:
            raise ConnectionError(f"Malformed auth ACK frame: {raw!r}") from e
        if frame.get("op") != "auth":
            raise ConnectionError(f"Expected auth ACK, got: {frame}")
        if frame.get("success") is False:
            raise AuthFailedError(
                f"WS auth failed: {frame.get('ret_msg') or 'unknown'}"
            )

    async def _keepalive_task(self):
        try:
            while True:
                await asyncio.sleep(PING_INTERVAL)
                if self.ws_state == WSState.EXITING:
                    # Terminal state (user close, auth fail, max reconnects) —
                    # exit instead of sleeping forever at PING_INTERVAL.
                    return
                if self.ws is None or self.ws_state != WSState.STREAMING:
                    continue
                await self.ws.send(self.custom_ping_message)
                if self._is_pong_stale():
                    logger.warning("Half-open connection detected — reconnecting")
                    self.ws_state = WSState.RECONNECTING
        except asyncio.CancelledError:
            logger.debug("Keepalive cancelled")
            return
        except (ConnectionClosed, ConnectionClosedError) as e:
            logger.warning(f"Keepalive: connection closed: {e}")
            self.ws_state = WSState.RECONNECTING
        except Exception:
            logger.exception("Keepalive failed")
            self.ws_state = WSState.RECONNECTING

    async def _open_conn(self):
        """Open a single websocket connection (with or without proxy)."""
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        if self.demo:
            subdomain = DEMO_SUBDOMAIN_TESTNET if self.testnet else DEMO_SUBDOMAIN_MAINNET
        endpoint = (
            self.url
            .replace("{SUBDOMAIN}", subdomain)
            .replace("{DOMAIN}", DOMAIN_MAIN)
            .replace("{TLD}", self.tld)
        )
        if self.proxy:
            # Lazy import so websockets_proxy is only required by proxy users.
            try:
                from websockets_proxy import Proxy, proxy_connect
            except ImportError as e:
                raise ImportError(
                    "websockets_proxy is required for proxy support. "
                    "Install with: pip install pybit[proxy]"
                ) from e
            logger.info(f"Connecting via proxy host: {_redact_proxy(self.proxy)}")
            conn = proxy_connect(
                endpoint,
                close_timeout=0.1,
                open_timeout=60,
                ping_interval=None,
                ping_timeout=None,
                proxy=Proxy.from_url(self.proxy),
            )
        else:
            logger.info("Connecting without proxy")
            conn = ws.connect(
                endpoint,
                close_timeout=0.1,
                open_timeout=60,
                ping_timeout=None,
                ping_interval=None,
            )
        # Only assign `_conn` after __aenter__ succeeds — otherwise a later
        # `_close_conn` would call __aexit__ on a never-entered context.
        try:
            self.ws = await conn.__aenter__()
        except BaseException:
            self.ws = None
            self._conn = None
            raise
        self._conn = conn

    async def _close_conn(self):
        """Cleanup ws + underlying connection object without racing state."""
        ws_obj, conn_obj = self.ws, self._conn
        self.ws, self._conn = None, None
        if ws_obj is not None:
            try:
                await ws_obj.close()
            except Exception:
                logger.exception("Error closing websocket")
        if conn_obj is not None:
            try:
                await conn_obj.__aexit__(None, None, None)
            except Exception:
                logger.exception("Error closing connection context")

    async def connect(self):
        """Establish the connection, authenticate if required, subscribe, and start loops.

        Single-frame reconnect loop — no recursion.
        """
        for attempt in range(self.MAX_RECONNECTS):
            try:
                # Tear down any previous connection before opening a new one.
                await self._close_conn()
                await self._open_conn()

                if self.api_key and self.api_secret:
                    await self._auth()

                # Reset state before subscriptions so incoming frames land correctly.
                self.ws_state = WSState.STREAMING
                self._last_pong = time.monotonic()

                if not self.subscription_message:
                    # Silently accepting this used to leave authenticated
                    # streams reading forever with nothing subscribed; log at
                    # INFO so a misconfigured caller notices.
                    logger.info(
                        "No subscription messages provided; stream will only "
                        "surface control frames"
                    )
                for msg in self.subscription_message:
                    await self.ws.send(msg)

                # (Re)start keepalive.
                if self._keepalive:
                    self._keepalive.cancel()
                self._keepalive = asyncio.create_task(self._keepalive_task())

                # Start the read loop once — subsequent reconnects reuse it.
                if self._handle_read_loop is None or self._handle_read_loop.done():
                    self._handle_read_loop = asyncio.create_task(self._read_loop())

                logger.info("Connected successfully")
                if self.downtime_callback is not None:
                    try:
                        result = self.downtime_callback()
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception:
                        logger.exception("Downtime callback error")
                return
            except asyncio.CancelledError:
                raise
            except AuthFailedError as e:
                # Bad credentials will never succeed on retry — surface the
                # error to the consumer and bail out. Retrying up to
                # MAX_RECONNECTS times risks Bybit rate-limiting the IP.
                logger.error(f"Auth failed, aborting: {e}")
                await self._enqueue({
                    "type": "terminal",
                    "reason": "auth_failed",
                    "success": False,
                    "ret_msg": str(e),
                    "op": "auth",
                })
                self.ws_state = WSState.EXITING
                if self._keepalive is not None:
                    self._keepalive.cancel()
                    self._keepalive = None
                return
            except Exception:
                logger.exception(f"Connect attempt {attempt + 1} failed")
                if self.ws_state == WSState.EXITING:
                    return
                wait = get_reconnect_wait(attempt)
                logger.info(
                    f"Reconnect in {wait}s "
                    f"({self.MAX_RECONNECTS - attempt - 1} attempts left)"
                )
                await asyncio.sleep(wait)

        # Exhausted attempts — inform consumer with a distinct sentinel.
        logger.error("Max reconnections reached")
        self.ws_state = WSState.EXITING
        # Cancel keepalive here — otherwise the task keeps sleeping at
        # PING_INTERVAL forever until close_connection() runs. Consumers who
        # treat the "Max reconnect reached" sentinel as authoritative and drop
        # the manager would otherwise leak the task.
        if self._keepalive is not None:
            self._keepalive.cancel()
            self._keepalive = None
        await self._enqueue({
            "type": "terminal",
            "reason": "max_reconnect",
            "success": False,
            "ret_msg": "Max reconnect reached",
        })

    async def _reconnect(self):
        """Trigger a reconnect from within the read loop or keepalive."""
        if self.ws_state == WSState.EXITING:
            return
        self.ws_state = WSState.RECONNECTING
        await self.connect()

    async def close_connection(self):
        """Fully tear down the connection, keepalive, and read loop.

        Idempotent — calling twice (e.g. explicit close then __aexit__)
        is a no-op after the first.
        """
        if self.ws_state == WSState.EXITING and self._keepalive is None \
                and self._handle_read_loop is None:
            return
        self.ws_state = WSState.EXITING

        if self._keepalive is not None:
            self._keepalive.cancel()
            try:
                await self._keepalive
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception("Error while shutting down keepalive")
            self._keepalive = None

        if self._handle_read_loop is not None:
            self._handle_read_loop.cancel()
            try:
                await self._handle_read_loop
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception("Error while shutting down read loop")
            self._handle_read_loop = None

        await self._close_conn()
        # Signal any pending recv() so consumer sees clean shutdown.
        await self._enqueue({
            "type": "terminal",
            "reason": "user_close",
            "success": True,
            "ret_msg": "connection closed by user",
        })

    async def recv(self, timeout: int = 5):
        try:
            return await asyncio.wait_for(self.queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None
