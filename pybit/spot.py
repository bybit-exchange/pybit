from ._http_manager import _HTTPManager
from ._websocket_stream import _SpotWebSocketManager
from ._websocket_stream import SPOT
from . import _helpers

from concurrent.futures import ThreadPoolExecutor


ws_name = SPOT
PUBLIC_V1_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/spot/quote/ws/v1"
PUBLIC_V2_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/spot/quote/ws/v2"
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/spot/ws"


class HTTP(_HTTPManager):
    def orderbook(self, **kwargs):
        """
        Get the orderbook.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-orderbook.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/quote/v1/depth"
        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs
        )

    def merged_orderbook(self, **kwargs):
        """
        Get the merged orderbook.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-mergedorderbook.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/quote/v1/depth/merged",
            query=kwargs
        )

    def query_kline(self, **kwargs):
        """
        Get kline.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-querykline.
        :returns: Request results as dictionary.
        """

        # Replace query param "from_time" since "from" keyword is reserved.
        # Temporary workaround until Bybit updates official request params
        if "from_time" in kwargs:
            kwargs["from"] = kwargs.pop("from_time")

        suffix = "/spot/quote/v1/kline"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs
        )

    def latest_information_for_symbol(self, **kwargs):
        """
        Get the latest information for symbol.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-latestsymbolinfo.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/quote/v1/ticker/24hr"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs
        )

    def last_traded_price(self, **kwargs):
        """
        Get the last traded price.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-lasttradedprice.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/quote/v1/ticker/price",
            query=kwargs
        )

    def best_bid_ask_price(self, **kwargs):
        """
        Get the best bid/ask price.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-bestbidask.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/quote/v1/ticker/book_ticker",
            query=kwargs
        )

    def public_trading_records(self, **kwargs):
        """
        Get recent trades. You can find a complete history of trades on Bybit
        at https://public.bybit.com/.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-publictradingrecords.
        :returns: Request results as dictionary.
        """

        # Replace query param "from_id" since "from" keyword is reserved.
        # Temporary workaround until Bybit updates official request params
        if "from_id" in kwargs:
            kwargs["from"] = kwargs.pop("from_id")

        suffix = "/spot/quote/v1/trades"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs
        )

    def query_symbol(self):
        """
        Get symbol info.

        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/symbols"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix
        )

    def place_active_order(self, **kwargs):
        """
        Places an active order. For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-activeorders.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-activeorders.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/order"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def place_active_order_bulk(self, orders: list, max_in_parallel=10):
        """
        Places multiple active orders in bulk using multithreading. For more
        information on place_active_order, see
        https://bybit-exchange.github.io/docs/spot/#t-activeorders.

        :param list orders: A list of orders and their parameters.
        :param max_in_parallel: The number of requests to be sent in parallel.
            Note that you are limited to 50 requests per second.
        :returns: Future request result dictionaries as a list.
        """

        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            executions = [
                executor.submit(
                    self.place_active_order,
                    **order
                ) for order in orders
            ]
        executor.shutdown()
        return [execution.result() for execution in executions]

    def get_active_order(self, **kwargs):
        """
        Gets an active order. For more information, see
        https://bybit-exchange.github.io/docs/spot/v1/#t-getactive.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/v1/#t-getactive.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/order"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def cancel_active_order(self, **kwargs):
        """
        Cancels an active order. For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-cancelactive.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-cancelactive.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/order"

        return self._submit_request(
            method="DELETE",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def fast_cancel_active_order(self, **kwargs):
        """
        Fast cancels an active order.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-fastcancelactiveorder.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="DELETE",
            path=self.endpoint + "/spot/v1/order/fast",
            query=kwargs,
            auth=True
        )

    def cancel_active_order_bulk(self, orders: list, max_in_parallel=10):
        """
        Cancels multiple active orders in bulk using multithreading. For more
        information on cancel_active_order, see
        https://bybit-exchange.github.io/docs/spot/#t-activeorders.

        :param list orders: A list of orders and their parameters.
        :param max_in_parallel: The number of requests to be sent in parallel.
            Note that you are limited to 50 requests per second.
        :returns: Future request result dictionaries as a list.
        """

        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            executions = [
                executor.submit(
                    self.cancel_active_order,
                    **order
                ) for order in orders
            ]
        executor.shutdown()
        return [execution.result() for execution in executions]

    def batch_cancel_active_order(self, **kwargs):
        """
        Batch cancels active orders.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-batchcancelactiveorder.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="DELETE",
            path=self.endpoint + "/spot/order/batch-cancel",
            query=kwargs,
            auth=True
        )

    def batch_fast_cancel_active_order(self, **kwargs):
        """
        Batch fast cancels active orders.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-batchfastcancelactiveorder.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="DELETE",
            path=self.endpoint + "/spot/order/batch-fast-cancel",
            query=kwargs,
            auth=True
        )

    def batch_cancel_active_order_by_ids(self, **kwargs):
        """
        Batch cancels active order by ids.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-batchcancelactiveorderbyids.
        :returns: Request results as dictionary.
        """

        return self._submit_request(
            method="DELETE",
            path=self.endpoint + "/spot/order/batch-cancel-by-ids",
            query=kwargs,
            auth=True
        )

    def query_active_order(self, **kwargs):
        """
        Query real-time active order information.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-queryactive.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/open-orders"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def user_trade_records(self, **kwargs):
        """
        Get user's trading records. The results are ordered in ascending order
        (the first item is the oldest).

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-usertraderecords.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/myTrades"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def get_wallet_balance(self, **kwargs):
        """
        Get wallet balance info.

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-balance.
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/account"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def server_time(self):
        """
        Get Bybit server time.

        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/time"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix
        )

    def borrow_margin_loan(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-borrowmarginloan
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/?python--pybit#t-borrowmarginloan
        :returns: Request result as integer.
        """

        suffix = "/spot/v1/cross-margin/loan"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def repay_margin_loan(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-repaymarginloan
        :param kwargs: See
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-repaymarginloan
        :returns: Request result as integer.
        """

        suffix = "/spot/v1/cross-margin/repay"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def query_borrowing_info(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryborrowinginfo

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryborrowinginfo
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/cross-margin/order"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def query_account_info(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryaccountinfo

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryaccountinfo
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/cross-margin/accounts/balance"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def query_interest_quota(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryinterestquota

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryinterestquota
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/cross-margin/loan-info"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def query_repayment_history(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryrepaymenthistory

        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/?python--pybit#t-queryrepaymenthistory
        :returns: Request results as dictionary.
        """

        suffix = "/spot/v1/cross-margin/repay/history"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def lt_asset_info(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-ltinfo
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-ltinfo
        :returns: Request results as Dictionary.
        """

        suffix = "/spot/lt/v1/info"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs
        )

    def lt_market_info(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-ltquotereference
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-ltquotereference
        :returns: Request results as Dictionary.
        """

        suffix = "/spot/lt/v1/reference"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def lt_purchase(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-ltpurchase
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-ltpurchase
        :returns: Request results as Dictionary.
        """

        suffix = "/spot/lt/v1/purchase"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def lt_redeem(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-ltredeem
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-ltredeem
        :returns: Request results as Dictionary.
        """

        suffix = "/spot/lt/v1/redeem"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def lt_purchase_redemption_history(self, **kwargs):
        """
        For more information, see
        https://bybit-exchange.github.io/docs/spot/#t-ltrecord
        :param kwargs: See
            https://bybit-exchange.github.io/docs/spot/#t-ltrecord
        :returns: Request results as Dictionary.
        """

        suffix = "/spot/lt/v1/record"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )


class WebSocket(_SpotWebSocketManager):
    def __init__(self, **kwargs):
        super().__init__(ws_name, **kwargs)

        self.ws_public_v1 = None
        self.ws_public_v2 = None
        self.ws_private = None
        self.active_connections = []
        self.kwargs = kwargs
        self.public_kwargs = _helpers.make_public_kwargs(self.kwargs)

    def is_connected(self):
        return self._are_connections_connected(self.active_connections)

    def _ws_public_v1_subscribe(self, topic, callback):
        if not self.ws_public_v1:
            self.ws_public_v1 = _SpotWebSocketManager(
                ws_name, **self.public_kwargs)
            self.ws_public_v1._connect(PUBLIC_V1_WSS)
            self.active_connections.append(self.ws_public_v1)
        self.ws_public_v1.subscribe(topic, callback)

    def _ws_public_v2_subscribe(self, topic, callback):
        if not self.ws_public_v2:
            self.ws_public_v2 = _SpotWebSocketManager(
                ws_name, **self.public_kwargs)
            self.ws_public_v2._connect(PUBLIC_V2_WSS)
            self.active_connections.append(self.ws_public_v2)
        self.ws_public_v2.subscribe(topic, callback)

    def _ws_private_subscribe(self, topic, callback):
        if not self.ws_private:
            self.ws_private = _SpotWebSocketManager(
                ws_name, **self.kwargs)
            self.ws_private._connect(PRIVATE_WSS)
            self.active_connections.append(self.ws_private)
        self.ws_private.subscribe(topic, callback)

    def custom_topic_stream(self, topic, callback, wss_url):
        subscribe = _helpers.identify_ws_method(
            wss_url,
            {
                PUBLIC_V1_WSS: self._ws_public_v1_subscribe,
                PUBLIC_V2_WSS: self._ws_public_v2_subscribe,
                PRIVATE_WSS: self._ws_private_subscribe
            })
        subscribe(topic, callback)

    def trade_v1_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websockettrade
        """
        topic = \
            {
                "topic": "trade",
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def realtimes_v1_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketrealtimes
        """
        topic = \
            {
                "topic": "realtimes",
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def kline_v1_stream(self, callback, symbol, interval):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketkline
        """
        topic = \
            {
                "topic": "kline_{}".format(str(interval)),
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def depth_v1_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketdepth
        """
        topic = \
            {
                "topic": "depth",
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def merged_depth_v1_stream(self, callback, symbol, dump_scale):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketmergeddepth
        """
        topic = \
            {
                "topic": "mergedDepth",
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "dumpScale": int(dump_scale),
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def diff_depth_v1_stream(self, callback, symbol):
        """
        This topic always returns messages in the "snapshot" format for a
        simplified user experience. pybit processes the delta/snapshot
        messages for you. Read the Bybit API documentation for more information.

        https://bybit-exchange.github.io/docs/spot/#t-websocketdiffdepth
        """
        topic = \
            {
                "topic": "diffDepth",
                "event": "sub",
                "symbol": symbol,
                "params": {
                    "binary": False
                }
            }
        self._ws_public_v1_subscribe(topic, callback)

    def depth_v2_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketv2depth
        """
        topic = \
            {
                "topic": "depth",
                "event": "sub",
                "params": {
                    "symbol": symbol,
                    "binary": False
                }
            }
        self._ws_public_v2_subscribe(topic, callback)

    def kline_v2_stream(self, callback, symbol, interval):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketv2kline
        """
        topic = \
            {
                "topic": "kline",
                "event": "sub",
                "params": {
                    "symbol": symbol,
                    "klineType": interval,
                    "binary": False
                }
            }
        self._ws_public_v2_subscribe(topic, callback)

    def trade_v2_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketv2trade
        """
        topic = \
            {
                "topic": "trade",
                "event": "sub",
                "params": {
                    "symbol": symbol,
                    "binary": False
                }
            }
        self._ws_public_v2_subscribe(topic, callback)

    def book_ticker_v2_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketv2bookticker
        """
        topic = \
            {
                "topic": "bookTicker",
                "event": "sub",
                "params": {
                    "symbol": symbol,
                    "binary": False
                }
            }
        self._ws_public_v2_subscribe(topic, callback)

    def realtimes_v2_stream(self, callback, symbol):
        """
        https://bybit-exchange.github.io/docs/spot/#t-websocketv2realtimes
        """
        topic = \
            {
                "topic": "realtimes",
                "event": "sub",
                "params": {
                    "symbol": symbol,
                    "binary": False
                }
            }
        self._ws_public_v2_subscribe(topic, callback)

    def outbound_account_info_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/spot/#t-outboundaccountinfo
        """
        topic = "outboundAccountInfo"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def execution_report_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/spot/#t-executionreport
        """
        topic = "executionReport"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def ticket_info_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/spot/#t-ticketinfo
        """
        topic = "ticketInfo"
        self._ws_private_subscribe(topic=topic, callback=callback)

