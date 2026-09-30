from ._http_manager import _V5HTTPManager
from .crypto_loan_flexible import CryptoLoanFlexible


class CryptoLoanFlexibleHTTP(_V5HTTPManager):
    def get_crypto_loan_flexible_available_inventory(self, **kwargs):
        """Get flexible crypto-loan available inventory.

        Required args:
            currency (string): Coin name, uppercase only

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/available-inventory
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoanFlexible.GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY}",
            query=kwargs,
            auth=True,
        )
