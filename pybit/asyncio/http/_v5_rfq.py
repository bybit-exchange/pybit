from pybit.asyncio.client import AsyncClient
from pybit.rfq import RFQ


class AsyncRFQHTTP(AsyncClient):
    async def create_rfq(self, **kwargs) -> dict:
        """Create a request for quote (RFQ).

        Required args:
            baseCoin (string): Base coin
            rfqType (string): RFQ type
            legs (array): Array of legs

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/create-rfq
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CREATE_RFQ}",
            query=kwargs,
            auth=True,
        )

    async def get_rfq_config(self, **kwargs) -> dict:
        """Get RFQ configuration.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/config
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_CONFIG}",
            query=kwargs,
            auth=True,
        )

    async def cancel_rfq(self, **kwargs) -> dict:
        """Cancel an RFQ.

        Required args:
            rfqId (string): RFQ ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/cancel-rfq
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CANCEL_RFQ}",
            query=kwargs,
            auth=True,
        )

    async def cancel_all_rfq(self, **kwargs) -> dict:
        """Cancel all RFQs.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/cancel-all-rfq
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CANCEL_ALL_RFQ}",
            query=kwargs,
            auth=True,
        )

    async def create_quote(self, **kwargs) -> dict:
        """Create a quote for an RFQ.

        Required args:
            rfqId (string): RFQ ID
            legs (array): Array of legs with prices

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/create-quote
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CREATE_QUOTE}",
            query=kwargs,
            auth=True,
        )

    async def execute_quote(self, **kwargs) -> dict:
        """Execute a quote.

        Required args:
            quoteId (string): Quote ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/execute-quote
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.EXECUTE_QUOTE}",
            query=kwargs,
            auth=True,
        )

    async def cancel_quote(self, **kwargs) -> dict:
        """Cancel a quote.

        Required args:
            quoteId (string): Quote ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/cancel-quote
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CANCEL_QUOTE}",
            query=kwargs,
            auth=True,
        )

    async def cancel_all_quotes(self, **kwargs) -> dict:
        """Cancel all quotes.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/cancel-all-quotes
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.CANCEL_ALL_QUOTES}",
            query=kwargs,
            auth=True,
        )

    async def get_rfq_realtime(self, **kwargs) -> dict:
        """Get active RFQs in realtime.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/rfq-realtime
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_RFQ_REALTIME}",
            query=kwargs,
            auth=True,
        )

    async def get_rfq_list(self, **kwargs) -> dict:
        """Get RFQ list history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/rfq-list
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_RFQ_LIST}",
            query=kwargs,
            auth=True,
        )

    async def get_quote_realtime(self, **kwargs) -> dict:
        """Get active quotes in realtime.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/quote-realtime
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_QUOTE_REALTIME}",
            query=kwargs,
            auth=True,
        )

    async def get_quote_list(self, **kwargs) -> dict:
        """Get quote list history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/quote-list
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_QUOTE_LIST}",
            query=kwargs,
            auth=True,
        )

    async def get_trade_list(self, **kwargs) -> dict:
        """Get RFQ trade list.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/trade-list
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_TRADE_LIST}",
            query=kwargs,
            auth=True,
        )

    async def get_public_trades(self, **kwargs) -> dict:
        """Get public RFQ trades.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/public-trades
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RFQ.GET_PUBLIC_TRADES}",
            query=kwargs,
        )

    async def accept_other_quote(self, **kwargs) -> dict:
        """Accept another market maker's quote.

        Required args:
            quoteId (string): Quote ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rfq/accept-other-quote
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RFQ.ACCEPT_OTHER_QUOTE}",
            query=kwargs,
            auth=True,
        )
