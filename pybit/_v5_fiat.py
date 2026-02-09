from ._http_manager import _V5HTTPManager
from .fiat import Fiat


class FiatHTTP(_V5HTTPManager):
    def get_fiat_coin_list(self, **kwargs):
        """Get the list of supported fiat coins.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/coin-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_COIN_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_fiat_reference_price(self, **kwargs):
        """Get the reference price for fiat trading.

        Required args:
            fiatCoin (string): Fiat coin name
            cryptoCoin (string): Crypto coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/reference-price
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_REFERENCE_PRICE}",
            query=kwargs,
            auth=True,
        )

    def request_fiat_quote(self, **kwargs):
        """Request a quote for fiat trading.

        Required args:
            fiatCoin (string): Fiat coin name
            cryptoCoin (string): Crypto coin name
            side (string): "buy" or "sell"
            size (string): Amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/quote-apply
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Fiat.REQUEST_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def execute_fiat_trade(self, **kwargs):
        """Execute a fiat trade based on a quote.

        Required args:
            quoteId (string): Quote ID from quote-apply

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-execute
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Fiat.EXECUTE_TRADE}",
            query=kwargs,
            auth=True,
        )

    def query_fiat_trade(self, **kwargs):
        """Query the status of a fiat trade.

        Required args:
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-query
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.QUERY_TRADE}",
            query=kwargs,
            auth=True,
        )

    def get_fiat_trade_history(self, **kwargs):
        """Get fiat trade history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_TRADE_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_fiat_balance(self, **kwargs):
        """Get fiat balance.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/balance-query
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_BALANCE}",
            query=kwargs,
            auth=True,
        )
