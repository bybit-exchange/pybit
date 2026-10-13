from enum import Enum


class InstitutionalLoan(str, Enum):
    GET_PRODUCT_INFO = "/v5/ins-loan/product-infos"
    GET_MARGIN_COIN_INFO = "/v5/ins-loan/ensure-tokens-convert"
    GET_LOAN_ORDERS = "/v5/ins-loan/loan-order"
    GET_REPAYMENT_ORDERS = "/v5/ins-loan/repaid-history"
    GET_LTV = "/v5/ins-loan/ltv-convert"
    BIND_OR_UNBIND_UID = "/v5/ins-loan/association-uid"
    REPAY_LOAN = "/v5/ins-loan/repay-loan"

    INS_LOAN_ASSOCIATION_UID = "/v5/ins-loan/association-uid"
    INS_LOAN_COIN_DELTA_AMOUNT = "/v5/ins-loan/coin-delta-amount"
    INS_LOAN_DELAY_LIQ_STATUS = "/v5/ins-loan/delay-liq-status"
    INS_LOAN_ENSURE_TOKENS = "/v5/ins-loan/ensure-tokens"
    INS_LOAN_ENSURE_TOKENS_CONVERT = "/v5/ins-loan/ensure-tokens-convert"
    INS_LOAN_GET_LOAN_ORDER = "/v5/ins-loan/loan-order"
    INS_LOAN_LTV_CONVERT = "/v5/ins-loan/ltv-convert"
    INS_LOAN_PRODUCT_INFOS = "/v5/ins-loan/product-infos"
    INS_LOAN_REPAID_HISTORY = "/v5/ins-loan/repaid-history"
    INS_LOAN_REPAY_LOAN = "/v5/ins-loan/repay-loan"
    def __str__(self) -> str:
        return self.value
