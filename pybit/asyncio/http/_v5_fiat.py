from pybit.asyncio.client import AsyncClient
from pybit.fiat import Fiat


class AsyncFiatHTTP(AsyncClient):
    async def get_fiat_coin_list(self, **kwargs) -> dict:
        """Get the list of supported fiat coins.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/coin-list
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_COIN_LIST}",
            query=kwargs,
            auth=True,
        )

    async def get_fiat_reference_price(self, **kwargs) -> dict:
        """Get the reference price for fiat trading.

        Required args:
            fiatCoin (string): Fiat coin name
            cryptoCoin (string): Crypto coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/reference-price
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_REFERENCE_PRICE}",
            query=kwargs,
            auth=True,
        )

    async def request_fiat_quote(self, **kwargs) -> dict:
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
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Fiat.REQUEST_QUOTE}",
            query=kwargs,
            auth=True,
        )

    async def execute_fiat_trade(self, **kwargs) -> dict:
        """Execute a fiat trade based on a quote.

        Required args:
            quoteId (string): Quote ID from quote-apply

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-execute
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Fiat.EXECUTE_TRADE}",
            query=kwargs,
            auth=True,
        )

    async def query_fiat_trade(self, **kwargs) -> dict:
        """Query the status of a fiat trade.

        Required args:
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-query
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.QUERY_TRADE}",
            query=kwargs,
            auth=True,
        )

    async def get_fiat_trade_history(self, **kwargs) -> dict:
        """Get fiat trade history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/trade-history
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_TRADE_HISTORY}",
            query=kwargs,
            auth=True,
        )

    async def get_fiat_balance(self, **kwargs) -> dict:
        """Get fiat balance.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/fiat/balance-query
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Fiat.GET_BALANCE}",
            query=kwargs,
            auth=True,
        )
