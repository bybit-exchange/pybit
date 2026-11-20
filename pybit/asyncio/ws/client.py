import json
from typing import (
    Optional,
    List
)
from uuid import uuid4

from pybit import exceptions
from pybit.unified_trading import (
    PRIVATE_WSS,
    PUBLIC_WSS,
    AVAILABLE_CHANNEL_TYPES,
)
from pybit.asyncio.ws.manager import AsyncWebsocketManager
from pybit.asyncio.ws.utils import chunks


class AsyncWebsocketClient:
    """
    Prepare payload for websocket connection
    """
    SPOT_MAX_CONNECTION_ARGS = 10
    # https://bybit-exchange.github.io/docs/v5/ws/connect
    # Bybit Spot can input up to 10 args for each subscription request sent to one connection

    def __init__(self,
                 channel_type: str,
                 testnet: bool,
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None,
                 proxy: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.proxy = proxy
        self.testnet = testnet
        self.channel_type = channel_type
        if channel_type not in AVAILABLE_CHANNEL_TYPES:
            raise exceptions.InvalidChannelTypeError(
                f"Channel type is not correct. Available: {AVAILABLE_CHANNEL_TYPES}")

        if channel_type == "private":
            self.WS_URL = PRIVATE_WSS
        else:
            self.WS_URL = PUBLIC_WSS.replace("{CHANNEL_TYPE}", channel_type)
            # Do not pass keys and attempt authentication on a public connection
            self.api_key = None
            self.api_secret = None

        if (self.api_key is None or self.api_secret is None) and channel_type == "private":
            raise exceptions.UnauthorizedExceptionError(
                "API_KEY or API_SECRET is not set. They both are needed in order to access private topics"
            )

    def spot_kline_stream(self, symbols: List[str]) -> AsyncWebsocketManager:
        # Prepare subscription message
        subscription_message = []
        for chunk in chunks(symbols, self.SPOT_MAX_CONNECTION_ARGS):
            subscription_message.append(
                json.dumps(
                    {
                        "op": "subscribe",
                        "req_id": str(uuid4()),
                        "args": chunk
                    }
                )
            )
        # Return instance of manager for further usages
        return AsyncWebsocketManager(
            channel_type=self.channel_type,
            url=PUBLIC_WSS.replace("{CHANNEL_TYPE}", self.channel_type),
            subscription_message=subscription_message,
            testnet=self.testnet,
        )

    def futures_kline_stream(self, symbols: List[str]) -> AsyncWebsocketManager:
        # Prepare subscription message
        subscription_message = json.dumps(
            {"op": "subscribe",
             "req_id": str(uuid4()),
             "args": symbols}
        )
        # Return instance of manager for further usages
        return AsyncWebsocketManager(
            channel_type=self.channel_type,
            url=PUBLIC_WSS.replace("{CHANNEL_TYPE}", self.channel_type),
            subscription_message=[subscription_message],
            testnet=self.testnet,
        )

    def user_futures_stream(self) -> AsyncWebsocketManager:
        subscription_message = json.dumps(
            {"op": "subscribe",
             "args": ["order.linear"]}
        )
        return AsyncWebsocketManager(
            channel_type=self.channel_type,
            url=PRIVATE_WSS,
            subscription_message=[subscription_message],
            testnet=self.testnet,
            api_key=self.api_key,
            api_secret=self.api_secret,
            proxy=self.proxy
        )

    def user_spot_stream(self) -> AsyncWebsocketManager:
        subscription_message = json.dumps(
            {"op": "subscribe",
             "args": ["order.spot"]}
        )
        return AsyncWebsocketManager(
            channel_type=self.channel_type,
            url=PRIVATE_WSS,
            subscription_message=[subscription_message],
            testnet=self.testnet,
            api_key=self.api_key,
            api_secret=self.api_secret,
            proxy=self.proxy
        )
