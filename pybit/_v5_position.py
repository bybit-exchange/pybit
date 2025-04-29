from ._http_manager import _V5HTTPManager
from .position import Position


class PositionHTTP(_V5HTTPManager):
    def get_positions(self, **kwargs):
        """Query real-time position data, such as position size, cumulative realizedPNL.

        Required args:
            category (string): Product type
                Unified account: linear, option
                Normal account: linear, inverse.

                Please note that category is not involved with business logic

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Position.GET_POSITIONS}",
            query=kwargs,
            auth=True,
        )

    def set_leverage(self, **kwargs):
        """Set the leverage

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name
            buyLeverage (string): [0, max leverage of corresponding risk limit].
                Note: Under one-way mode, buyLeverage must be the same as sellLeverage
            sellLeverage (string): [0, max leverage of corresponding risk limit].
                Note: Under one-way mode, buyLeverage must be the same as sellLeverage

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/leverage
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    def switch_margin_mode(self, **kwargs):
        """Select cross margin mode or isolated margin mode

        Required args:
            category (string): Product type. linear,inverse

                Please note that category is not involved with business logicUnified account is not applicable
            symbol (string): Symbol name
            tradeMode (integer): 0: cross margin. 1: isolated margin
            buyLeverage (string): The value must be equal to sellLeverage value
            sellLeverage (string): The value must be equal to buyLeverage value

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/cross-isolate
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SWITCH_MARGIN_MODE}",
            query=kwargs,
            auth=True,
        )

    def set_tp_sl_mode(self, **kwargs):
        """Set TP/SL mode to Full or Partial

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name
            tpSlMode (string): TP/SL mode. Full,Partial

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/tpsl-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_TP_SL_MODE}",
            query=kwargs,
            auth=True,
        )

    def switch_position_mode(self, **kwargs):
        """
        It supports to switch the position mode for USDT perpetual and Inverse futures.
        If you are in one-way Mode, you can only open one position on Buy or Sell side.
        If you are in hedge mode, you can open both Buy and Sell side positions simultaneously.

        Required args:
            category (string): Product type. linear,inverse

                Please note that category is not involved with business logicUnified account is not applicable

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/position-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SWITCH_POSITION_MODE}",
            query=kwargs,
            auth=True,
        )

    def set_risk_limit(self, **kwargs):
        """
        The risk limit will limit the maximum position value you can hold under different margin requirements.
        If you want to hold a bigger position size, you need more margin. This interface can set the risk limit of a single position.
        If the order exceeds the current risk limit when placing an order, it will be rejected. Click here to learn more about risk limit.

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name
            riskId (integer): Risk limit ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/set-risk-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_RISK_LIMIT}",
            query=kwargs,
            auth=True,
        )

    def set_trading_stop(self, **kwargs):
        """Set the take profit, stop loss or trailing stop for the position.

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/trading-stop
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_TRADING_STOP}",
            query=kwargs,
            auth=True,
        )

    def set_auto_add_margin(self, **kwargs):
        """Turn on/off auto-add-margin for isolated margin position

        Required args:
            category (string): Product type. linear
            symbol (string): Symbol name
            autoAddMargin (integer): Turn on/off. 0: off. 1: on

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/auto-add-margin
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_AUTO_ADD_MARGIN}",
            query=kwargs,
            auth=True,
        )

    def add_or_reduce_margin(self, **kwargs):
        """Manually add or reduce margin for isolated margin position

        Required args:
            category (string): Product type. linear
            symbol (string): Symbol name
            margin (string): Add or reduce. To add, use 10. To reduce, use -10

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/manual-add-margin
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.ADD_MARGIN}",
            query=kwargs,
            auth=True,
        )

    def get_executions(self, **kwargs):
        """Query users' execution records, sorted by execTime in descending order

        Required args:
            category (string):
                Product type Unified account: spot, linear, option
                Normal account: linear, inverse.

                Please note that category is not involved with business logic

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/order/execution
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Position.GET_EXECUTIONS}",
            query=kwargs,
            auth=True,
        )

    def get_closed_pnl(self, **kwargs):
        """Query user's closed profit and loss records. The results are sorted by createdTime in descending order.

        Required args:
            category (string):
                Product type Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/position/close-pnl
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Position.GET_CLOSED_PNL}",
            query=kwargs,
            auth=True,
        )
