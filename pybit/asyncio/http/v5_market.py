from pybit.asyncio.client import AsyncClient
from pybit.market import Market


class AsyncMarketHTTP(AsyncClient):
    async def get_server_time(self) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/time
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_SERVER_TIME}"
        )

    async def get_kline(self, **kwargs) -> dict:
        """Query the kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type: spot,linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/kline
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_KLINE}",
            query=kwargs,
        )
