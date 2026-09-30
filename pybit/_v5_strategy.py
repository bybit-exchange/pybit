from ._http_manager import _V5HTTPManager
from .strategy import Strategy


class StrategyHTTP(_V5HTTPManager):
    def _create_typed_strategy(self, strategy_type, **kwargs):
        supplied_type = kwargs.get("strategyType", strategy_type)
        if supplied_type != strategy_type:
            raise ValueError(
                f"Strategy helper requires strategyType={strategy_type}; "
                f"received {supplied_type}"
            )
        kwargs["strategyType"] = strategy_type
        return self.create_strategy(**kwargs)

    def create_strategy(self, **kwargs):
        """Create a Chase Order, TWAP, Iceberg, or POV strategy.

        Required args:
            category (string): Product type for the trading pair.
            symbol (string): Trading pair symbol.
            side (string): Order direction.
            strategyType (string): chaseOrder, twap, iceberg, or pov.

        Type-specific args:
            Refer to the API documentation for the required sizing and execution
            parameters of the selected strategy type.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/create-strategy
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Strategy.CREATE_STRATEGY}",
            query=kwargs,
            auth=True,
        )

    def create_chase_order_strategy(self, **kwargs):
        """Create a Chase Order strategy.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/create-strategy
        """
        return self._create_typed_strategy("chaseOrder", **kwargs)

    def create_twap_strategy(self, **kwargs):
        """Create a TWAP strategy.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/create-strategy
        """
        return self._create_typed_strategy("twap", **kwargs)

    def create_iceberg_strategy(self, **kwargs):
        """Create an Iceberg strategy.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/create-strategy
        """
        return self._create_typed_strategy("iceberg", **kwargs)

    def create_pov_strategy(self, **kwargs):
        """Create a POV strategy.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/create-strategy
        """
        return self._create_typed_strategy("pov", **kwargs)

    def query_strategy_list(self, **kwargs):
        """Query trading strategy list with filters.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/strategy/strategy-list
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
            https://bybit-exchange.github.io/docs/v5/strategy/order-list
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
            https://bybit-exchange.github.io/docs/v5/strategy/stop-strategy
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Strategy.STOP_STRATEGY}",
            query=kwargs,
            auth=True,
        )
