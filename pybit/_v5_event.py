from ._http_manager import _V5HTTPManager
from .event import Event


class EventHTTP(_V5HTTPManager):
    def get_ec_instruments_info(self, **kwargs):
        """Get Event Contract instrument information.

        Optional args:
            symbol (string): Symbol name, e.g.
                ETHUSDT-28AUG26-2450-2570-OUT.
            status (string): Instrument status: PreLaunch, Trading, Delivering, or Closed.
            limit (integer): Items per page. Default: 50; range: 1 to 100.
            cursor (string): Pagination cursor. Use nextPageCursor from the previous response.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/market/instrument-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_INSTRUMENTS_INFO}",
            query=kwargs,
        )

    def get_ec_orderbook(self, **kwargs):
        """Get the 25-level Event Contract orderbook.

        Required args:
            symbol (string): Symbol name.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/market/orderbook
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Event.GET_EC_ORDERBOOK}",
            query=kwargs,
        )

    def submit_ec_quote(self, **kwargs):
        """Submit an Event Contract quote.

        Required args:
            symbol (string): Symbol name.
            orderLinkId (string): User-defined order ID.
            grossPayoutRatio (string): Gross payout ratio.
            amount (string): Quote amount in the settlement coin.

        Optional args:
            cancelAfterMs (integer): Automatic cancellation delay in
                milliseconds. 0 uses the instrument's quoteMaxValidMs; a
                non-zero value must not exceed quoteMaxValidMs.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/submit-quote
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Event.SUBMIT_EC_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def cancel_ec_quote(self, **kwargs):
        """Cancel an Event Contract quote.

        Optional args:
            orderLinkId (string): User-defined order ID.
            orderId (string): Order ID.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/cancel-quote
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Event.CANCEL_EC_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def cancel_all_ec_quotes(self, **kwargs):
        """Cancel all Event Contract quotes for a symbol.

        Required args:
            symbol (string): Symbol name.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/event/trade/cancel-all
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Event.CANCEL_ALL_EC_QUOTES}",
            query=kwargs,
            auth=True,
        )

    def get_ec_order_history(self, **kwargs):
        """Get Event Contract Order History

        Optional args:
            symbol (string): Symbol name.
            orderId (string): Order ID.
            orderLinkId (string): User-defined order ID.
            startTime (integer): Start time in milliseconds. Default: 7 days ago.
            endTime (integer): End time in milliseconds. Default: now.
            limit (integer): Items per page. Default: 50; range: 1 to 100.
            cursor (string): Pagination cursor.

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

        Optional args:
            symbol (string): Symbol name.
            orderId (string): Order ID. Takes priority over orderLinkId.
            orderLinkId (string): User-defined order ID.
            limit (integer): Items per page. Default: 20; range: 1 to 50.
            cursor (string): Pagination cursor.

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

        Optional args:
            symbol (string): Symbol name. If omitted, returns all positions.
            baseCoin (string): Base coin filter.
            settleCoin (string): Settlement coin filter.
            limit (integer): Items per page. Default: 20; range: 1 to 50.
            cursor (string): Pagination cursor.

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

        Optional args:
            orderId (string): Order ID filter.
            startTime (integer): Start time in milliseconds. Default: 7 days ago.
            endTime (integer): End time in milliseconds. Default: now.
            limit (integer): Items per page. Default: 50; range: 1 to 100.
            cursor (string): Pagination cursor.

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

        Optional args:
            orderId (string): Order ID filter.
            orderLinkId (string): User-defined order ID.
            startTime (integer): Start time in milliseconds. Default: 7 days ago.
            endTime (integer): End time in milliseconds. Default: now.
            limit (integer): Items per page. Default: 50; range: 1 to 100.
            cursor (string): Pagination cursor.

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
