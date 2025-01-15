from ._async_http_manager import _V5ASYNCHTTPManager
from ..institutional_loan import InstitutionalLoan as InsLoan


class InstitutionalLoanASYNCHTTP(_V5ASYNCHTTPManager):
    async def get_product_info(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/margin-product-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_PRODUCT_INFO}",
            query=kwargs,
        )

    async def get_margin_coin_info(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/margin-coin-convert-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    async def get_loan_orders(self, **kwargs) -> dict:
        """
        Get loan orders information

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/loan-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LOAN_ORDERS}",
            query=kwargs,
            auth=True,
        )

    async def get_repayment_info(self, **kwargs) -> dict:
        """
        Get a list of your loan repayment orders (orders which repaid the loan).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/repay-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_REPAYMENT_ORDERS}",
            query=kwargs,
            auth=True,
        )

    async def get_ltv(self, **kwargs) -> dict:
        """
        Get your loan-to-value ratio.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/ltv-convert
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LTV}",
            query=kwargs,
            auth=True,
        )

    async def bind_or_unbind_uid(self, **kwargs) -> dict:
        """
        For the institutional loan product, you can bind new UIDs to the risk
        unit or unbind UID from the risk unit.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/otc/bind-uid
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{InsLoan.BIND_OR_UNBIND_UID}",
            query=kwargs,
            auth=True,
        )
