from enum import Enum


class Account(str, Enum):
    GET_WALLET_BALANCE = "/v5/account/wallet-balance"
    GET_TRANSFERABLE_AMOUNT = "/v5/account/withdrawal"
    UPGRADE_TO_UNIFIED_ACCOUNT = "/v5/account/upgrade-to-uta"
    GET_BORROW_HISTORY = "/v5/account/borrow-history"
    REPAY_LIABILITY = "/v5/account/quick-repayment"
    GET_COLLATERAL_INFO = "/v5/account/collateral-info"
    SET_COLLATERAL_COIN = "/v5/account/set-collateral-switch"
    BATCH_SET_COLLATERAL_COIN = "/v5/account/set-collateral-switch-batch"
    GET_COIN_GREEKS = "/v5/asset/coin-greeks"
    GET_FEE_RATE = "/v5/account/fee-rate"
    GET_ACCOUNT_INFO = "/v5/account/info"
    GET_TRANSACTION_LOG = "/v5/account/transaction-log"
    GET_CONTRACT_TRANSACTION_LOG = "/v5/account/contract-transaction-log"
    SET_MARGIN_MODE = "/v5/account/set-margin-mode"
    SET_MMP = "/v5/account/mmp-modify"
    RESET_MMP = "/v5/account/mmp-reset"
    GET_MMP_STATE = "/v5/account/mmp-state"
    SET_NO_CONVERT_REPAY = "/v5/account/no-convert-repay"
    BORROW = "/v5/account/borrow"
    GET_INSTRUMENTS_INFO = "/v5/account/instruments-info"
    REPAY = "/v5/account/repay"
    QUERY_DCP_INFO = "/v5/account/query-dcp-info"
    SET_HEDGING_MODE = "/v5/account/set-hedging-mode"
    GET_SMP_GROUP = "/v5/account/smp-group"
    GET_USER_SETTING_CONFIG = "/v5/account/user-setting-config"
    SET_LIMIT_PRICE_ACTION = "/v5/account/set-limit-px-action"

    def __str__(self) -> str:
        return self.value
