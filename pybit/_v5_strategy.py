from ._http_manager import _V5HTTPManager
from .strategy import Strategy


class StrategyHTTP(_V5HTTPManager):
    def create_chase_order_strategy(self, **kwargs):
        """Create Chase Order strategy for dynamic price tracking.

        Required args:
            category (string): Product type for the trading pair.
            symbol (string): Trading pair symbol.
            side (string): Order direction.
            size (string): Total quantity to execute.
            strategyType (string): Strategy type identifier.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Strategy.CREATE_CHASE_ORDER_STRATEGY}",
            query=kwargs,
            auth=True,
        )

    def query_strategy_list(self, **kwargs):
        """Query trading strategy list with filters.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Strategy.QUERY_STRATEGY_LIST}",
            query=kwargs,
            auth=True,
        )

    def query_strategy_order_list(self, **kwargs):
        """Query orders created by a specific strategy.

        Required args:
            strategyId (string): Strategy ID to query orders for (UUID format).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Strategy.QUERY_STRATEGY_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def stop_strategy(self, **kwargs):
        """Stop a running strategy.

        Required args:
            strategyId (string): Strategy ID to stop (UUID format).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Strategy.STOP_STRATEGY}",
            query=kwargs,
            auth=True,
        )
