from ._http_manager import _V5HTTPManager
from ._websocket_stream import _V5WebSocketManager
from .spread import Spread


WSS_NAME = "Spread Trading"
PUBLIC_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/v5/public/spread"


class SpreadHTTP(_V5HTTPManager):
    def get_instruments_info(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/market/instrument
        """
        request = self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_INSTRUMENTS_INFO}",
            query=kwargs,
        )
        return request

    def get_orderbook(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/market/orderbook
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_ORDERBOOK}",
            query=kwargs,
        )

    def get_tickers(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/market/tickers
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_TICKERS}",
            query=kwargs,
        )

    def get_public_trade_history(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/market/recent-trade
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_PUBLIC_TRADING_HISTORY}",
            query=kwargs,
        )

    def place_order(self, **kwargs) -> dict:
        """
        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name
            side (string): Buy, Sell
            orderType (string): Market, Limit
            qty (string): Order quantity
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/create-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Spread.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def amend_order(self, **kwargs) -> dict:
        """
        Required args:
            symbol (string): Spread combination symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/amend-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Spread.AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_order(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/cancel-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Spread.CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_all_orders(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/cancel-all
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Spread.CANCEL_ALL_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_open_orders(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/open-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_OPEN_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_order_history(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/order-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_trade_history(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spread/trade/trade-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Spread.GET_TRADE_HISTORY}",
            query=kwargs,
            auth=True,
        )


class _V5WebSocketSpreadTrading(_V5WebSocketManager):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(WSS_NAME, **kwargs)
        self.WS_URL = PUBLIC_WSS
        self.start(self.WS_URL)
