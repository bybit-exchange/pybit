from ._http_manager import _V5HTTPManager
from .event import Event


class EventHTTP(_V5HTTPManager):
    def get_ec_order_history(self, **kwargs):
        """Get Event Contract Order History
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/order-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_ec_active_orders(self, **kwargs):
        """Get Event Contract Active Orders
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/open-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_ACTIVE_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_ec_position_info(self, **kwargs):
        """Get Event Contract Position Info
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_POSITION_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_ec_settlements(self, **kwargs):
        """Get Event Contract Settlement Records

        Required args:
            symbol (string): Symbol name, e.g. `BTCUSDT-EC`
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/settlement
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_SETTLEMENTS}",
            query=kwargs,
            auth=True,
        )

    def get_ec_trade_history(self, **kwargs):
        """Get Event Contract Trade History

        Required args:
            symbol (string): Symbol name, e.g. `BTCUSDT-EC`
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/execution
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_TRADE_HISTORY}",
            query=kwargs,
            auth=True,
        )
