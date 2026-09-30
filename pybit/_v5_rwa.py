from ._http_manager import _V5HTTPManager
from .rwa import RWA


class RWAHTTP(_V5HTTPManager):
    def get_convert_detail(self, **kwargs):
        """Get Convert order details.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-detail
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_CONVERT_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_convert_list(self, **kwargs):
        """Get the list of available Convert pairs.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_CONVERT_LIST}",
            query=kwargs,
            auth=True,
        )

    def submit_convert(self, **kwargs):
        """Submit a Convert order to mint or redeem stock tokens.

        Required args:
            convertType (string): MINT converts stock to token; REDEEM converts
                token to stock.
            symbol (string): Underlying stock symbol, e.g. `AAPL-US`.
            inputAmount (string): Stock amount for MINT or token amount for REDEEM.
            frontMultiplier (string): Client-side multiplier snapshot validated by
                the server.
            requestId (string): Idempotency key, unique for 24 hours per MM account.
            flow (string): Request flow type.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-submit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.SUBMIT_CONVERT}",
            query=kwargs,
            auth=True,
        )

    def get_multiplier_list(self, **kwargs):
        """Get the stock-token multiplier list.

        Required args:
            current (integer): Page number, starting from 1.
            pageSize (integer): Number of records per page. Default: 10.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/multiplier-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_MULTIPLIER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_market_session(self, **kwargs):
        """Get the trading calendar and current market status.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/market-session
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_MARKET_SESSION}",
            query=kwargs,
            auth=True,
        )

    def place_stocks_order(self, **kwargs):
        """Place an order to buy or sell stocks.

        Required args:
            symbol (string): Stock symbol, e.g. `TSLA-US` or `AAPL-US`.
            quoteToken (string): Quote asset. Currently only `USDC` is supported.
            side (string): Order side.
            type (string): Order type.
            timeInForce (string): Time-in-force policy.
            orderTime (integer): Client order timestamp in milliseconds.
            requestId (string): Idempotency key, unique for 24 hours per MM account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.PLACE_STOCKS_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_stocks_order(self, **kwargs):
        """Cancel a stock order.

        Required args:
            orderNo (string): System order number.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/cancel-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.CANCEL_STOCKS_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_stocks_order_detail(self, **kwargs):
        """Get stock order details.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/order-detail
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_STOCKS_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_stocks_positions(self, **kwargs):
        """Get all stock positions.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/positions
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_STOCKS_POSITIONS}",
            query=kwargs,
            auth=True,
        )
