import json
from typing import (
    Optional,
    List,
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


class AsyncWebsocketClient:
    """Factory for `AsyncWebsocketManager` instances scoped to a channel type."""

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

    def spot_kline_stream(self, topics: List[str]) -> AsyncWebsocketManager:
        """Public spot stream.

        Bybit Spot limits each subscribe frame to
        :attr:`SPOT_MAX_CONNECTION_ARGS` args, so this splits ``topics`` into
        chunks and sends one subscribe frame per chunk.

        Args:
            topics: Full Bybit topic strings, e.g.
                ``["kline.60.BTCUSDT", "orderbook.1.ETHUSDT"]``.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/public/kline
        """
        subscription_message = []
        for chunk in chunks(topics, self.SPOT_MAX_CONNECTION_ARGS):
            subscription_message.append(json.dumps({
                "op": "subscribe",
                "req_id": str(uuid4()),
                "args": chunk,
            }))
        return self._manager(self._public_url(), subscription_message, private=False)

    def futures_kline_stream(self, topics: List[str]) -> AsyncWebsocketManager:
        """Public linear / inverse / option stream.

        Args:
            topics: Full Bybit topic strings, e.g.
                ``["kline.60.BTCUSDT", "publicTrade.ETHUSDT"]``. Use
                ``channel_type`` to select the product surface.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/public/kline
        """
        subscription_message = json.dumps({
            "op": "subscribe",
            "req_id": str(uuid4()),
            "args": topics,
        })
        return self._manager(self._public_url(), [subscription_message], private=False)

    def user_futures_stream(self) -> AsyncWebsocketManager:
        """Private stream — order updates for linear contracts.

        Requires ``channel_type='private'`` and valid keys.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/order
        """
        self._require_private("user_futures_stream")
        subscription_message = json.dumps({
            "op": "subscribe",
            "args": ["order.linear"],
        })
        return self._manager(PRIVATE_WSS, [subscription_message], private=True)

    def user_spot_stream(self) -> AsyncWebsocketManager:
        """Private stream — order updates for spot.

        Requires ``channel_type='private'`` and valid keys.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/websocket/private/order
        """
        self._require_private("user_spot_stream")
        subscription_message = json.dumps({
            "op": "subscribe",
            "args": ["order.spot"],
        })
        return self._manager(PRIVATE_WSS, [subscription_message], private=True)
