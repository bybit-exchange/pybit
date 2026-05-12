import logging
from pybit.asyncio.client import AsyncClient
from pybit.crypto_loan import CryptoLoan

logger = logging.getLogger(__name__)


class AsyncCryptoLoanHTTP(AsyncClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.crypto_loan_legacy_message = (
            "Crypto Loan (Legacy) endpoints are deprecated. See new docs under "
            "Crypto Loan (New): "
            "https://bybit-exchange.github.io/docs/v5/new-crypto-loan/loan-coin"
        )

    # Crypto Loan (Legacy)

    async def get_collateral_coins(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/collateral-coin
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_COLLATERAL_COINS}",
            query=kwargs,
        )

    async def get_borrowable_coins(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/loan-coin
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWABLE_COINS}",
            query=kwargs,
        )

    async def get_account_borrowable_or_collateralizable_limit(self, **kwargs) -> dict:
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
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_ACCOUNT_BORROWABLE_OR_COLLATERALIZABLE_LIMIT}",
            query=kwargs,
            auth=True,
        )

    async def borrow_crypto_loan(self, **kwargs) -> dict:
        """
        Required args:
            loanCurrency (string): Loan coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/borrow
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.BORROW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def repay_crypto_loan(self, **kwargs) -> dict:
        """
        Required args:
            orderId (string): Loan order ID
            amount (string): Repay amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.REPAY_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_unpaid_loans(self, **kwargs) -> dict:
        """
        Query for your ongoing loans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_UNPAID_LOANS}",
            query=kwargs,
            auth=True,
        )

    async def get_loan_repayment_history(self, **kwargs) -> dict:
        """
        Query for loan repayment transactions. A loan may be repaid in multiple
        repayments.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/repay-transaction
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LOAN_REPAYMENT_HISTORY}",
            query=kwargs,
            auth=True,
        )

    async def get_completed_loan_history(self, **kwargs) -> dict:
        """
        Query for the last 6 months worth of your completed (fully paid off)
        loans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/completed-loan-order
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_COMPLETED_LOAN_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    async def get_max_allowed_collateral_reduction_amount(self, **kwargs) -> dict:
        """
        Query for the maximum amount by which collateral may be reduced by.

        Required args:
            currency (string): Collateral coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_MAX_ALLOWED_COLLATERAL_REDUCTION_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    async def adjust_collateral_amount(self, **kwargs) -> dict:
        """
        You can increase or reduce your collateral amount. When you reduce,
        please obey the max. allowed reduction amount.

        Required args:
            currency (string): Collateral coin
            amount (string): Adjustment amount
            direction (string): 0: add collateral; 1: reduce collateral

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/adjust-collateral
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.ADJUST_COLLATERAL_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    async def get_crypto_loan_ltv_adjustment_history(self, **kwargs) -> dict:
        """
        You can increase or reduce your collateral amount. When you reduce,
        please obey the max. allowed reduction amount.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/crypto-loan/ltv-adjust-history
        """
        logger.warning(self.crypto_loan_legacy_message)
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_CRYPTO_LOAN_LTV_ADJUSTMENT_HISTORY}",
            query=kwargs,
            auth=True,
        )

    # Crypto Loan (New)

    async def get_borrowable_coins_new_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/loan-coin
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWABLE_COINS_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_collateral_coins_new_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/collateral-coin
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_COLLATERAL_COINS_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_max_allowed_collateral_reduction_amount_new_crypto_loan(self, **kwargs) -> dict:
        """
        Retrieve the maximum redeemable amount of your collateral asset based on LTV.

        Required args:
            currency (string): Collateral coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/reduce-max-collateral-amt
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_MAX_ALLOWED_COLLATERAL_REDUCTION_AMOUNT_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def adjust_collateral_amount_new_crypto_loan(self, **kwargs) -> dict:
        """
        You can increase or reduce your collateral amount. When you reduce, please obey the Get Max. Allowed Collateral Reduction Amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/adjust-collateral
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.ADJUST_COLLATERAL_AMOUNT_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_ltv_adjustment_history_new_crypto_loan(self, **kwargs) -> dict:
        """
        Query for your LTV adjustment history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/ltv-adjust-history
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LTV_ADJUSTMENT_HISTORY_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_crypto_loan_ltv_adjustment_history_new_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/ltv-adjust-history
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LTV_ADJUSTMENT_HISTORY_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_position_new_crypto_loan(self):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/crypto-loan-position
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_POSITION_NEW_CRYPTO_LOAN}",
            auth=True,
        )

    async def borrow_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Required args:
            loanCurrency (string): Loan coin name
            loanAmount (string): Amount to borrow

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/borrow
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.BORROW_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def repay_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Fully or partially repay a loan. If interest is due, that is paid off
        first, with the loaned amount being paid off only after due interest.

        Required args:
            loanCurrency (string): Loan coin name
            loanAmount (string): Repay amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.REPAY_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def collateral_repayment_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Required args:
            loanCurrency (string): Loan coin name
            collateralCoin (string): Amount to borrow
            amount (string): Amount to borrow

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay-collateral
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.COLLATERAL_REPAYMENT_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_flexible_loans_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Query for your ongoing loans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/unpaid-loan-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_FLEXIBLE_LOANS_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_borrowing_history_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/loan-orders
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWING_HISTORY_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_repayment_history_flexible_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay-orders
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_REPAYMENT_HISTORY_FLEXIBLE_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_lending_market_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        If you want to lend, you can use this endpoint to check whether there
        are any suitable counterparty borrow orders available.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-market
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LENDING_MARKET_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_borrowing_market_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        If you want to borrow, you can use this endpoint to check whether there
        are any suitable counterparty supply orders available.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-market
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWING_MARKET_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def borrow_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.BORROW_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def renew_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/renew
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.RENEW_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def create_lending_order_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.CREATE_LENDING_ORDER_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def create_borrowing_order_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-borrow
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.CREATE_BORROWING_ORDER_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def cancel_lending_order_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-supply
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.CANCEL_LENDING_ORDER_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_borrowing_contract_info_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-contract
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWING_CONTRACT_INFO_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_lending_contract_info_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-contract%20copy
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LENDING_CONTRACT_INFO_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_borrowing_orders_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_BORROWING_ORDERS_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_renewal_orders_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/renew-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_RENEWAL_ORDERS_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_lending_orders_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_LENDING_ORDERS_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def repay_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.REPAY_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def collateral_repayment_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-collateral
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.COLLATERAL_REPAYMENT_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_repayment_history_fixed_crypto_loan(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-history
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoan.GET_REPAYMENT_HISTORY_FIXED_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )

    async def get_max_loan_amount_new_crypto_loan(self, **kwargs) -> dict:
        """
        Required args:
            currency (string): Coin to borrow

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/max-loan-amt
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{CryptoLoan.GET_MAX_LOAN_AMOUNT_NEW_CRYPTO_LOAN}",
            query=kwargs,
            auth=True,
        )
