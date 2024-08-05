from pybit.asyncio._http_manager import _AsyncV5HTTPManager
from pybit.broker import Broker


class AsyncBrokerHTTP(_AsyncV5HTTPManager):
    async def get_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/earning
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )
