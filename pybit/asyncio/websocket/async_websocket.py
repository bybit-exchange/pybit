import json
from uuid import uuid4
from typing import (
    Optional,
    List
)

from pybit import exceptions
from pybit.unified_trading import (
    PUBLIC_WSS,
    PRIVATE_WSS,
    AVAILABLE_CHANNEL_TYPES
)
from pybit.asyncio.websocket.async_manager import AsyncWebsocketManager


class AsyncWebsocket:
    """
    Prepare payload for websocket connection
    """

    def __init__(self,
                 testnet: bool,
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

    @staticmethod
    def _check_channel_type(channel_type: str):
        if channel_type not in AVAILABLE_CHANNEL_TYPES:
            raise exceptions.InvalidChannelTypeError(
                f"Channel type is not correct. Available: {AVAILABLE_CHANNEL_TYPES}")

    def _check_api_key_for_private_channel(self, channel_type: str = "private"):
        if (self.api_key is None or self.api_secret is None) and channel_type == "private":
            raise exceptions.UnauthorizedExceptionError(
                "API_KEY or API_SECRET is not set. They both are needed in order to access private topics"
            )

    def _prepare_public_subscription(self, symbols: List[str]) -> str:
        return json.dumps(
            {"op": "subscribe",
             "req_id": str(uuid4()),  # Optional but can help handle multiple subscriptions
             "args": symbols
             }
        )

    def _prepare_private_trade_subscription(self, topic: str, category: str) -> str:
        return json.dumps(
            {"op": "subscribe",
             "args": [f"{topic}.{category}"]}
        )

    def _get_public_async_manager(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        self._check_channel_type(channel_type)
        return AsyncWebsocketManager(channel_type=channel_type,
                                     testnet=self.testnet,
                                     url=PUBLIC_WSS.replace("{CHANNEL_TYPE}", channel_type),
                                     subscription_message=self._prepare_public_subscription(symbols))

    def _get_private_async_manager(self, topic: str, category: str) -> AsyncWebsocketManager:
        self._check_api_key_for_private_channel()
        return AsyncWebsocketManager(channel_type="private",
                                     testnet=self.testnet,
                                     url=PRIVATE_WSS,
                                     subscription_message=self._prepare_private_trade_subscription(topic, category),
                                     api_key=self.api_key,
                                     api_secret=self.api_secret)

    def orderbook_stream(self, symbols, channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def trade_stream(self, symbols, channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def kline_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def ticker_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def liquidation_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def lt_kline_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def lt_ticker_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def li_nav_stream(self, symbols: List[str], channel_type: str) -> AsyncWebsocketManager:
        return self._get_public_async_manager(symbols, channel_type)

    def order_stream(self, category: str) -> AsyncWebsocketManager:
        return self._get_private_async_manager("order", category)

    def position_stream(self, category: str) -> AsyncWebsocketManager:
        return self._get_private_async_manager("position", category)

    def execution_stream(self, category: str) -> AsyncWebsocketManager:
        return self._get_private_async_manager("execution", category)

    def execution_fast_stream(self, category: str) -> AsyncWebsocketManager:
        return self._get_private_async_manager("execution.fast", category)

    def wallet_stream(self) -> AsyncWebsocketManager:
        self._check_api_key_for_private_channel()
        subscription_message = json.dumps(
            {"op": "subscribe",
             "args": ["wallet"]}
        )
        return AsyncWebsocketManager(channel_type="private",
                                     testnet=self.testnet,
                                     url=PRIVATE_WSS,
                                     subscription_message=subscription_message,
                                     api_key=self.api_key,
                                     api_secret=self.api_secret)

    def greeks_stream(self, ) -> AsyncWebsocketManager:
        self._check_api_key_for_private_channel()
        subscription_message = json.dumps(
            {"op": "subscribe",
             "args": ["greeks"]}
        )
        return AsyncWebsocketManager(channel_type="private",
                                     testnet=self.testnet,
                                     url=PRIVATE_WSS,
                                     subscription_message=subscription_message,
                                     api_key=self.api_key,
                                     api_secret=self.api_secret)
