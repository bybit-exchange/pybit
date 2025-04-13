from ._http_manager import _V5HTTPManager
from .crypto_loan import CryptoLoan


class CryptoLoanHTTP(_V5HTTPManager):
    def get_collateral_coins(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/collateral-coin
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_COLLATERAL_COINS}",
            query=kwargs,
        )

    def get_borrowable_coins(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/loan-coin
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWABLE_COINS}",
            query=kwargs,
        )

    def get_account_borrowable_or_collateralizable_limit(self, **kwargs):
        """
        Query for the minimum and maximum amounts your account can borrow and
        how much collateral you can put up.

        Required args:
            loanCurrency (string): Loan coin name
            collateralCurrency (string): Collateral coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/acct-borrow-collateral
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_ACCOUNT_BORROWABLE_OR_COLLATERALIZABLE_LIMIT}",
            query=kwargs,
            auth=True,
        )

    def borrow_crypto_loan(self, **kwargs):
        """
        Required args:
            loanCurrency (string): Loan coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/borrow
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.BORROW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    def repay_crypto_loan(self, **kwargs):
        """
        Required args:
            orderId (string): Loan order ID
            amount (string): Repay amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.REPAY_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    def get_unpaid_loans(self, **kwargs):
        """
        Query for your ongoing loans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_UNPAID_LOANS}",
            query=kwargs,
            auth=True,
        )

    def get_loan_repayment_history(self, **kwargs):
        """
        Query for loan repayment transactions. A loan may be repaid in multiple
        repayments.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay-transaction
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LOAN_REPAYMENT_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_completed_loan_history(self, **kwargs):
        """
        Query for the last 6 months worth of your completed (fully paid off)
        loans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/completed-loan-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_COMPLETED_LOAN_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_max_allowed_collateral_reduction_amount(self, **kwargs):
        """
        Query for the maximum amount by which collateral may be reduced by.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_MAX_ALLOWED_COLLATERAL_REDUCTION_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def adjust_collateral_amount(self, **kwargs):
        """
        You can increase or reduce your collateral amount. When you reduce,
        please obey the max. allowed reduction amount.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/adjust-collateral
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.ADJUST_COLLATERAL_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def get_crypto_loan_ltv_adjustment_history(self, **kwargs):
        """
        You can increase or reduce your collateral amount. When you reduce,
        please obey the max. allowed reduction amount.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/ltv-adjust-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_CRYPTO_LOAN_LTV_ADJUSTMENT_HISTORY}",
            query=kwargs,
            auth=True,
        )
