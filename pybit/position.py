from enum import Enum


class Position(str, Enum):
    GET_POSITIONS = "/v5/position/list"
    SET_LEVERAGE = "/v5/position/set-leverage"
    SWITCH_MARGIN_MODE = "/v5/position/switch-isolated"
    SET_TP_SL_MODE = "/v5/position/set-tpsl-mode"
    SWITCH_POSITION_MODE = "/v5/position/switch-mode"
    SET_RISK_LIMIT = "/v5/position/set-risk-limit"
    SET_TRADING_STOP = "/v5/position/trading-stop"
    SET_AUTO_ADD_MARGIN = "/v5/position/set-auto-add-margin"
    ADD_MARGIN = "/v5/position/add-margin"
    GET_EXECUTIONS = "/v5/execution/list"
    GET_CLOSED_PNL = "/v5/position/closed-pnl"

    def __str__(self) -> str:
        return self.value
