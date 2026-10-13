from ._http_manager import _V5HTTPManager
from .institutional_loan import InstitutionalLoan as InsLoan


class InstitutionalLoanHTTP(_V5HTTPManager):
    def get_product_info(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/margin-product-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_PRODUCT_INFO}",
            query=kwargs,
        )

    def get_margin_coin_info(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/margin-coin-convert-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    def get_loan_orders(self, **kwargs) -> dict:
        """
        Get loan orders information

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/loan-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LOAN_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_repayment_info(self, **kwargs) -> dict:
        """
        Get a list of your loan repayment orders (orders which repaid the loan).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/repay-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_REPAYMENT_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_ltv(self, **kwargs) -> dict:
        """
        Get your loan-to-value ratio.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/ltv-convert
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LTV}",
            query=kwargs,
            auth=True,
        )

    def bind_or_unbind_uid(self, **kwargs) -> dict:
        """
        For the institutional loan product, you can bind new UIDs to the risk
        unit or unbind UID from the risk unit.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/bind-uid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{InsLoan.BIND_OR_UNBIND_UID}",
            query=kwargs,
            auth=True,
        )

    def repay_loan(self, **kwargs) -> dict:
        """
        Repay the institutional loan.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/repay-loan
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{InsLoan.REPAY_LOAN}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_association_uid(self, **kwargs):
        """Bind/Unbind UID

        Required args:
            uid (string): The UID to bind or unbind.
            operate (string): Operation type. `0`: Bind, `1`: Unbind.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/association-uid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_ASSOCIATION_UID}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_coin_delta_amount(self, **kwargs):
        """Get Coin Delta Amount
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/coin-delta-amount
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_COIN_DELTA_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_delay_liq_status(self, **kwargs):
        """Get Delay Liquidation Status
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/delay-liq-status
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_DELAY_LIQ_STATUS}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_ensure_tokens(self, **kwargs):
        """Get Margin Tokens
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/ensure-tokens
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_ENSURE_TOKENS}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_ensure_tokens_convert(self, **kwargs):
        """Get Margin Token Conversion Details
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/ensure-tokens-convert
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_ENSURE_TOKENS_CONVERT}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_get_loan_order(self, **kwargs):
        """Get Loan Orders
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/loan-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_GET_LOAN_ORDER}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_ltv_convert(self, **kwargs):
        """Get LTV with Conversion Details
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/ltv-convert
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_LTV_CONVERT}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_product_infos(self, **kwargs):
        """Get Product Infos
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/product-infos
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_PRODUCT_INFOS}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_repaid_history(self, **kwargs):
        """Get Repaid History
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/repaid-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_REPAID_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def ins_loan_repay_loan(self, **kwargs):
        """Repay Loan

        Required args:
            token (string): Repayment coin name, uppercase only. e.g. `USDT`, `BTC`.
            quantity (string): Repayment quantity.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/ins-loan/repay-loan
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{InstitutionalLoan.INS_LOAN_REPAY_LOAN}",
            query=kwargs,
            auth=True,
        )
