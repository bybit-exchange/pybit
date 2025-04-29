from enum import Enum


class CryptoLoan(str, Enum):
    GET_COLLATERAL_COINS = "/v5/crypto-loan/collateral-data"
    GET_BORROWABLE_COINS = "/v5/crypto-loan/loanable-data"
    GET_ACCOUNT_BORROWABLE_OR_COLLATERALIZABLE_LIMIT = "/v5/crypto-loan/borrowable-collateralisable-number"
    BORROW_CRYPTO_LOAN = "/v5/crypto-loan/borrow"
    REPAY_CRYPTO_LOAN = "/v5/crypto-loan/repay"
    GET_UNPAID_LOANS = "/v5/crypto-loan/ongoing-orders"
    GET_LOAN_REPAYMENT_HISTORY = "/v5/crypto-loan/repayment-history"
    GET_COMPLETED_LOAN_ORDER_HISTORY = "/v5/crypto-loan/borrow-history"
    GET_MAX_ALLOWED_COLLATERAL_REDUCTION_AMOUNT = "/v5/crypto-loan/max-collateral-amount"
    ADJUST_COLLATERAL_AMOUNT = "/v5/crypto-loan/adjust-ltv"
    GET_CRYPTO_LOAN_LTV_ADJUSTMENT_HISTORY = "/v5/crypto-loan/adjustment-history"

    def __str__(self) -> str:
        return self.value
