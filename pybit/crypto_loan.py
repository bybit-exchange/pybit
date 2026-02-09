from enum import Enum


class CryptoLoan(str, Enum):
    # Crypto Loan (Legacy)
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

    # Crypto Loan (New); common to both Flexible and Fixed loans
    GET_BORROWABLE_COINS_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/loanable-data"
    GET_COLLATERAL_COINS_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/collateral-data"
    GET_MAX_ALLOWED_COLLATERAL_REDUCTION_AMOUNT_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/max-collateral-amount"
    ADJUST_COLLATERAL_AMOUNT_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/adjust-ltv"
    GET_LTV_ADJUSTMENT_HISTORY_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/adjustment-history"
    GET_POSITION_NEW_CRYPTO_LOAN = "/v5/crypto-loan-common/position"

    # Flexible loans
    BORROW_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/borrow"
    REPAY_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/repay"
    COLLATERAL_REPAYMENT_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/repay-collateral"
    GET_FLEXIBLE_LOANS_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/ongoing-coin"
    GET_BORROWING_HISTORY_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/borrow-history"
    GET_REPAYMENT_HISTORY_FLEXIBLE_CRYPTO_LOAN = "/v5/crypto-loan-flexible/repayment-history"

    # Fixed loans
    GET_LENDING_MARKET_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/supply-order-quote"
    GET_BORROWING_MARKET_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/borrow-order-quote"
    BORROW_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/borrow"
    RENEW_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/renew"
    CREATE_LENDING_ORDER_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/supply"
    CREATE_BORROWING_ORDER_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/borrow-order-cancel"
    CANCEL_LENDING_ORDER_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/supply-order-cancel"
    GET_BORROWING_CONTRACT_INFO_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/borrow-contract-info"
    GET_LENDING_CONTRACT_INFO_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/supply-contract-info"
    GET_BORROWING_ORDERS_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/borrow-order-info"
    GET_RENEWAL_ORDERS_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/renew-info"
    GET_LENDING_ORDERS_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/supply-order-info"
    REPAY_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/fully-repay"
    COLLATERAL_REPAYMENT_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/repay-collateral"
    GET_REPAYMENT_HISTORY_FIXED_CRYPTO_LOAN = "/v5/crypto-loan-fixed/repayment-history"

    def __str__(self) -> str:
        return self.value
