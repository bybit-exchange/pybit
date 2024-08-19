from ._async_http_manager import _V5ASYNCHTTPManager
from ..broker import Broker


class BrokerHTTP(_V5ASYNCHTTPManager):
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
