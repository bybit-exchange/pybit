import json
from typing import (
    List,
    Optional,
    Union,
)
from uuid import uuid4

from pybit import exceptions
from pybit.asyncio.ws.manager import AsyncWebsocketManager
from pybit.asyncio.ws.utils import chunks


# Locally-owned constants — avoid pulling pybit.unified_trading, which
# transitively imports the sync websocket + HTTP stack.
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.{TLD}/v5/private"
# Use {TLD} so non-.com tlds (nl / kz / com.hk / …) route correctly. The
# original hardcoded ".com" silently ignored the tld kwarg.
PUBLIC_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.{TLD}/v5/public/{CHANNEL_TYPE}"
AVAILABLE_CHANNEL_TYPES = [
    "inverse",
    "linear",
    "spot",
    "option",
    "misc/status",
    "private",
]


# Topics that ignore the ``{symbol}`` placeholder (no per-symbol fan-out).
_TOPIC_NO_SYMBOL = frozenset({
    "position",
    "order",
    "execution",
    "wallet",
    "greeks",
    "spread.order",
    "spread.execution",
    "system.status",
})


class AsyncWebsocketClient:
    """Factory for :class:`AsyncWebsocketManager` instances scoped to a channel.

    Terminal frame contract (returned by ``await mgr.recv()``):
      - Normal stream frames carry a ``"topic"`` field (Bybit payload).
      - Control ACKs carry an ``"op"`` field (``"subscribe"``, ``"auth"``).
      - Terminal sentinels — emitted exactly once when the stream is done —
        carry ``"type": "terminal"`` and always include ``success`` +
        ``ret_msg``:
          - Max-reconnect exhaustion: ``success=False, reason="max_reconnect"``.
          - Auth rejection:           ``success=False, reason="auth_failed"``.
          - User close:               ``success=True,  reason="user_close"``.
      Consumers can use ``frame.get("type") == "terminal"`` as an
      authoritative "the stream is done" signal instead of guessing.
    """

    # https://bybit-exchange.github.io/docs/v5/ws/connect
    # Bybit Spot can input up to 10 args for each subscription request sent to one connection
    SPOT_MAX_CONNECTION_ARGS = 10

    def __init__(
            self,
            channel_type: str,
            testnet: bool,
            demo: bool = False,
            api_key: Optional[str] = None,
            api_secret: Optional[str] = None,
            rsa_authentication: bool = False,
            proxy: Optional[str] = None,
            tld: str = "com",
            private_auth_expire: int = 1,
    ):
        self.testnet = testnet
        self.demo = demo
        self.channel_type = channel_type
        self.rsa_authentication = rsa_authentication
        self.proxy = proxy
        self.tld = tld
        self.private_auth_expire = private_auth_expire

        if channel_type not in AVAILABLE_CHANNEL_TYPES:
            raise exceptions.InvalidChannelTypeError(
                f"Channel type is not correct. Available: {AVAILABLE_CHANNEL_TYPES}"
            )

        if channel_type == "private":
            self.api_key = api_key
            self.api_secret = api_secret
            if not self.api_key or not self.api_secret:
                raise exceptions.UnauthorizedExceptionError(
                    "API_KEY or API_SECRET is not set. They both are needed in order to access private topics"
                )
        else:
            # Don't attempt authentication on public connections.
            self.api_key = None
            self.api_secret = None

    def _require_private(self, method_name: str) -> None:
        if self.channel_type != "private":
            raise exceptions.InvalidChannelTypeError(
                f"{method_name} requires channel_type='private'; "
                f"got channel_type={self.channel_type!r}"
            )

    def _require_public(self, method_name: str) -> None:
        if self.channel_type in ("private", "misc/status"):
            raise exceptions.InvalidChannelTypeError(
                f"{method_name} requires a public channel_type "
                f"(linear/inverse/spot/option); got channel_type="
                f"{self.channel_type!r}"
            )

    def _require_system(self, method_name: str) -> None:
        if self.channel_type != "misc/status":
            raise exceptions.InvalidChannelTypeError(
                f"{method_name} requires channel_type='misc/status'; "
                f"got channel_type={self.channel_type!r}"
            )

    def _public_url(self) -> str:
        return PUBLIC_WSS.replace("{CHANNEL_TYPE}", self.channel_type)

    def _manager(self, url: str, subscription_message: List[str], private: bool) -> AsyncWebsocketManager:
        return AsyncWebsocketManager(
            channel_type=self.channel_type,
            url=url,
            subscription_message=subscription_message,
            testnet=self.testnet,
            demo=self.demo,
            rsa_authentication=self.rsa_authentication,
            api_key=self.api_key if private else None,
            api_secret=self.api_secret if private else None,
            proxy=self.proxy,
            tld=self.tld,
            private_auth_expire=self.private_auth_expire,
        )

    @staticmethod
    def _expand_topic(topic_template: str, symbol: Union[str, List[str], None]) -> List[str]:
        """Fan out ``topic_template`` over one or more symbols.

        ``topic_template`` uses the sync-compatible ``{symbol}`` placeholder.
        Topics that ignore ``{symbol}`` (e.g. ``"position"``, ``"wallet"``)
        return a single-element list unchanged.
        """
        if topic_template in _TOPIC_NO_SYMBOL:
            return [topic_template]
        if isinstance(symbol, str):
            symbols = [symbol]
        else:
            symbols = list(symbol or [])
        if not symbols:
            raise ValueError(f"topic {topic_template!r} needs at least one symbol")
        return [topic_template.format(symbol=s) for s in symbols]

    def _subscription_messages(self, args: List[str]) -> List[str]:
        """Build subscribe frames, chunking to spot's per-frame arg limit.

        Non-spot channels ship a single frame; spot channels split into
        chunks of ``SPOT_MAX_CONNECTION_ARGS`` so the server accepts them.
        """
        if self.channel_type == "spot":
            batches = list(chunks(args, self.SPOT_MAX_CONNECTION_ARGS))
        else:
            batches = [args] if args else []
        return [
            json.dumps({"op": "subscribe", "req_id": str(uuid4()), "args": b})
            for b in batches
        ]

    def _manager_from_topic(
            self,
            topic_template: str,
            symbol: Union[str, List[str], None],
            private: bool,
    ) -> AsyncWebsocketManager:
        args = self._expand_topic(topic_template, symbol)
        url = PRIVATE_WSS if private else self._public_url()
        return self._manager(url, self._subscription_messages(args), private=private)

    # ------------------------------------------------------------------
    # Raw / low-level helpers (kept for callers that already build topic
    # strings themselves).
    # ------------------------------------------------------------------

    def spot_kline_stream(self, topics: List[str]) -> AsyncWebsocketManager:
        """Raw public spot subscribe: pass full Bybit topic strings.

        Bybit Spot limits each subscribe frame to
        :attr:`SPOT_MAX_CONNECTION_ARGS` args, so this splits ``topics`` into
        chunks and sends one subscribe frame per chunk.
        """
        return self._manager(
            self._public_url(), self._subscription_messages(list(topics)),
            private=False,
        )

    def futures_kline_stream(self, topics: List[str]) -> AsyncWebsocketManager:
        """Raw public linear / inverse / option subscribe: full topic strings."""
        return self._manager(
            self._public_url(), self._subscription_messages(list(topics)),
            private=False,
        )

    # ------------------------------------------------------------------
    # Private streams — require channel_type='private'.
    # ------------------------------------------------------------------

    def position_stream(self) -> AsyncWebsocketManager:
        """Position updates in real-time.

        https://bybit-exchange.github.io/docs/v5/websocket/private/position
        """
        self._require_private("position_stream")
        return self._manager_from_topic("position", None, private=True)

    def order_stream(self) -> AsyncWebsocketManager:
        """Order updates in real-time.

        https://bybit-exchange.github.io/docs/v5/websocket/private/order
        """
        self._require_private("order_stream")
        return self._manager_from_topic("order", None, private=True)

    def execution_stream(self) -> AsyncWebsocketManager:
        """Execution updates in real-time.

        https://bybit-exchange.github.io/docs/v5/websocket/private/execution
        """
        self._require_private("execution_stream")
        return self._manager_from_topic("execution", None, private=True)

    def fast_execution_stream(self, categorised_topic: str = "") -> AsyncWebsocketManager:
        """Low-latency execution stream with a limited set of trade types.

        ``categorised_topic`` is appended after ``execution.fast.`` to filter
        by ``category`` — see the docs for valid values.

        https://bybit-exchange.github.io/docs/v5/websocket/private/fast-execution
        """
        self._require_private("fast_execution_stream")
        topic = "execution.fast"
        if categorised_topic:
            topic = f"{topic}.{categorised_topic}"
        # Single-arg subscribe — don't route through _TOPIC_NO_SYMBOL.
        return self._manager(
            PRIVATE_WSS, self._subscription_messages([topic]), private=True,
        )

    def wallet_stream(self) -> AsyncWebsocketManager:
        """Wallet balance updates in real-time.

        https://bybit-exchange.github.io/docs/v5/websocket/private/wallet
        """
        self._require_private("wallet_stream")
        return self._manager_from_topic("wallet", None, private=True)

    def greek_stream(self) -> AsyncWebsocketManager:
        """Option greeks updates in real-time.

        https://bybit-exchange.github.io/docs/v5/websocket/private/greek
        """
        self._require_private("greek_stream")
        return self._manager_from_topic("greeks", None, private=True)

    def spread_order_stream(self) -> AsyncWebsocketManager:
        """Spread trading order updates.

        https://bybit-exchange.github.io/docs/v5/spread/websocket/private/order
        """
        self._require_private("spread_order_stream")
        return self._manager_from_topic("spread.order", None, private=True)

    def spread_execution_stream(self) -> AsyncWebsocketManager:
        """Spread trading execution updates.

        https://bybit-exchange.github.io/docs/v5/spread/websocket/private/execution
        """
        self._require_private("spread_execution_stream")
        return self._manager_from_topic("spread.execution", None, private=True)

    # Preserved for parity with the initial async release, which only
    # exposed these two private helpers. They now delegate to
    # ``order_stream`` — a Bybit v5 private ``order`` subscription surfaces
    # linear and spot updates on the same connection.
    def user_futures_stream(self) -> AsyncWebsocketManager:
        """Deprecated alias — use :meth:`order_stream`."""
        self._require_private("user_futures_stream")
        # ``order.linear`` is the historical filter form; keep it working
        # for callers already on the initial release.
        subscription_message = json.dumps({
            "op": "subscribe",
            "req_id": str(uuid4()),
            "args": ["order.linear"],
        })
        return self._manager(PRIVATE_WSS, [subscription_message], private=True)

    def user_spot_stream(self) -> AsyncWebsocketManager:
        """Deprecated alias — use :meth:`order_stream`."""
        self._require_private("user_spot_stream")
        subscription_message = json.dumps({
            "op": "subscribe",
            "req_id": str(uuid4()),
            "args": ["order.spot"],
        })
        return self._manager(PRIVATE_WSS, [subscription_message], private=True)

    # ------------------------------------------------------------------
    # Public streams — require a public channel_type.
    # ------------------------------------------------------------------

    def orderbook_stream(
            self, depth: int, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Orderbook updates at the requested depth.

        Depth support varies per channel — see docs for the matrix.

        https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
        """
        self._require_public("orderbook_stream")
        return self._manager_from_topic(
            "orderbook.{depth}.{symbol}".format(depth=depth, symbol="{symbol}"),
            symbol, private=False,
        )

    def rpi_orderbook_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Retail Price Improvement orderbook stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook-rpi
        """
        self._require_public("rpi_orderbook_stream")
        return self._manager_from_topic(
            "orderbook.rpi.{symbol}", symbol, private=False,
        )

    def trade_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Public trades stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/trade
        """
        self._require_public("trade_stream")
        return self._manager_from_topic(
            "publicTrade.{symbol}", symbol, private=False,
        )

    def ticker_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Ticker stream — best-bid/ask + last-price snapshots.

        https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
        """
        self._require_public("ticker_stream")
        return self._manager_from_topic(
            "tickers.{symbol}", symbol, private=False,
        )

    def kline_stream(
            self, interval: int, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Kline (candle) stream at the requested interval.

        https://bybit-exchange.github.io/docs/v5/websocket/public/kline
        """
        self._require_public("kline_stream")
        return self._manager_from_topic(
            "kline.{interval}.{symbol}".format(interval=interval, symbol="{symbol}"),
            symbol, private=False,
        )

    def all_liquidation_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """All-liquidations stream (500ms push, all liquidations on Bybit).

        Prefer this over the deprecated ``liquidation`` stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/all-liquidation
        """
        self._require_public("all_liquidation_stream")
        return self._manager_from_topic(
            "allLiquidation.{symbol}", symbol, private=False,
        )

    def lt_kline_stream(
            self, interval: int, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Leveraged-token kline stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline
        """
        self._require_public("lt_kline_stream")
        return self._manager_from_topic(
            "kline_lt.{interval}.{symbol}".format(interval=interval, symbol="{symbol}"),
            symbol, private=False,
        )

    def lt_ticker_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Leveraged-token ticker stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker
        """
        self._require_public("lt_ticker_stream")
        return self._manager_from_topic(
            "tickers_lt.{symbol}", symbol, private=False,
        )

    def lt_nav_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Leveraged-token NAV stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/etp-nav
        """
        self._require_public("lt_nav_stream")
        return self._manager_from_topic(
            "lt.{symbol}", symbol, private=False,
        )

    def insurance_pool_stream(
            self, contract_group: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Insurance pool stream (per contract group, e.g. ``"USDT"``).

        https://bybit-exchange.github.io/docs/v5/websocket/public/insurance-pool
        """
        self._require_public("insurance_pool_stream")
        return self._manager_from_topic(
            "insurance.{symbol}", contract_group, private=False,
        )

    def price_limit_stream(
            self, symbol: Union[str, List[str]],
    ) -> AsyncWebsocketManager:
        """Order price-limit stream.

        https://bybit-exchange.github.io/docs/v5/websocket/public/order-price-limit
        """
        self._require_public("price_limit_stream")
        return self._manager_from_topic(
            "priceLimit.{symbol}", symbol, private=False,
        )

    # ------------------------------------------------------------------
    # System status stream — requires channel_type='misc/status'.
    # ------------------------------------------------------------------

    def system_status_stream(self) -> AsyncWebsocketManager:
        """Platform maintenance / service-incident status feed.

        https://bybit-exchange.github.io/docs/v5/websocket/system/system-status
        """
        self._require_system("system_status_stream")
        return self._manager_from_topic("system.status", None, private=False)
