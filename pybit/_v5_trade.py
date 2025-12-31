from ._http_manager import _V5HTTPManager
from .trade import Trade


class TradeHTTP(_V5HTTPManager):
    def place_order(self, **kwargs):
        """This method supports to create the order for spot, spot margin, linear perpetual, inverse futures and options.

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name
            side (string): Buy, Sell
            orderType (string): Market, Limit
            qty (string): Order quantity
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def amend_order(self, **kwargs):
        """Unified account covers: Linear contract / Options
        Normal account covers: USDT perpetual / Inverse perpetual / Inverse futures

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/amend-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_order(self, **kwargs):
        """Unified account covers: Spot / Linear contract / Options
        Normal account covers: USDT perpetual / Inverse perpetual / Inverse futures

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name
            orderId (string): Order ID. Either orderId or orderLinkId is required
            orderLinkId (string): User customised order ID. Either orderId or orderLinkId is required

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/cancel-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_open_orders(self, **kwargs):
        """Query unfilled or partially filled orders in real-time. To query older order records, please use the order history interface.

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/open-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Trade.GET_OPEN_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def cancel_all_orders(self, **kwargs):
        """Cancel all open orders

        Required args:
            category (string): Product type
                Unified account: spot, linear, option
                Normal account: linear, inverse.

                Please note that category is not involved with business logic. If cancel all by baseCoin, it will cancel all linear & inverse orders

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/cancel-all
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ALL_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_order_history(self, **kwargs):
        """Query order history. As order creation/cancellation is asynchronous, the data returned from this endpoint may delay.
        If you want to get real-time order information, you could query this endpoint or rely on the websocket stream (recommended).

        Required args:
            category (string): Product type
                Unified account: spot, linear, option
                Normal account: linear, inverse.

                Please note that category is not involved with business logic

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/order-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Trade.GET_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def place_batch_order(self, **kwargs):
        """Covers: Option (Unified Account)

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name
            > side (string): Buy, Sell
            > orderType (string): Market, Limit
            > qty (string): Order quantity

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/batch-place
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def amend_batch_order(self, **kwargs):
        """Covers: Option (Unified Account)

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name
            > orderId (string): Order ID. Either orderId or orderLinkId is required
            > orderLinkId (string): User customised order ID. Either orderId or orderLinkId is required

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/batch-amend
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_batch_order(self, **kwargs):
        """This endpoint allows you to cancel more than one open order in a single request.

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/batch-cancel
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_borrow_quota(self, **kwargs):
        """Query the qty and amount of borrowable coins in spot account.

        Required args:
            category (string): Product type. spot
            symbol (string): Symbol name
            side (string): Transaction side. Buy,Sell

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/spot-borrow-quota
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Trade.GET_BORROW_QUOTA}",
            query=kwargs,
            auth=True,
        )

    def set_dcp(self, **kwargs):
        """Covers: Option (Unified Account)

        Required args:
            timeWindow (integer): Disconnection timing window time. [10, 300], unit: second

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/dcp
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.SET_DCP}",
            query=kwargs,
            auth=True,
        )

    def pre_check_order(self, **kwargs):
        """This endpoint is used to calculate the changes in IMR and MMR of
        UTA account before and after placing an order.

        Required args:
            category (string): Product type Unified account: spot, linear,
                option. Normal account: linear, inverse. Please note that
                category is not involved with business logic
            symbol (string): Symbol name
            side (string): Buy, Sell
            orderType (string): Market, Limit
            qty (string): Order quantity

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/pre-check-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PRE_CHECK_ORDER}",
            query=kwargs,
            auth=True,
        )
