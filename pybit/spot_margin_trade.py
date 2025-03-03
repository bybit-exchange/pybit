from enum import Enum


class SpotMarginTrade(str, Enum):
    # UTA endpoints
    TOGGLE_MARGIN_TRADE = "/v5/spot-margin-trade/switch-mode"
    SET_LEVERAGE = "/v5/spot-margin-trade/set-leverage"
    VIP_MARGIN_DATA = "/v5/spot-margin-trade/data"
    STATUS_AND_LEVERAGE = "/v5/spot-margin-trade/state"
    HISTORICAL_INTEREST = "/v5/spot-margin-trade/interest-rate-history"
    # normal mode (non-UTA) endpoints
    NORMAL_GET_VIP_MARGIN_DATA = "/v5/spot-cross-margin-trade/data"
    NORMAL_GET_MARGIN_COIN_INFO = "/v5/spot-cross-margin-trade/pledge-token"
    NORMAL_GET_BORROWABLE_COIN_INFO = "/v5/spot-cross-margin-trade/borrow-token"
    NORMAL_GET_INTEREST_QUOTA = "/v5/spot-cross-margin-trade/loan-info"
    NORMAL_GET_LOAN_ACCOUNT_INFO = "/v5/spot-cross-margin-trade/account"
    NORMAL_BORROW = "/v5/spot-cross-margin-trade/loan"
    NORMAL_REPAY = "/v5/spot-cross-margin-trade/repay"
    NORMAL_GET_BORROW_ORDER_DETAIL = "/v5/spot-cross-margin-trade/orders"
    NORMAL_GET_REPAYMENT_ORDER_DETAIL = "/v5/spot-cross-margin-trade/repay-history"
    NORMAL_TOGGLE_MARGIN_TRADE = "/v5/spot-cross-margin-trade/switch"

    def __str__(self) -> str:
        return self.value
