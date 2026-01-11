from pybit.asyncio.client import AsyncClient
from pybit.broker import Broker


class AsyncBrokerHTTP(AsyncClient):
    async def get_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/earning
        """
        self.logger.warning(
            "get_broker_earnings() is deprecated. See get_exchange_broker_earnings().")

        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )

    async def get_exchange_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-earning
        """

        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_EXCHANGE_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )
