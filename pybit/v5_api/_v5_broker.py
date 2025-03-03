from pybit._http_manager import _V5HTTPManager
from pybit.broker import Broker


class BrokerHTTP(_V5HTTPManager):
    def get_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/earning
        """
        self.logger.warning(
            "get_broker_earnings() is deprecated. See get_exchange_broker_earnings().")

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )

    def get_exchange_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-earning
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_EXCHANGE_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )
