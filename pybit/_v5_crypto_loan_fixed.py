from ._http_manager import _V5HTTPManager
from .crypto_loan_fixed import CryptoLoanFixed


class CryptoLoanFixedHTTP(_V5HTTPManager):
    def get_crypto_loan_fixed_available_inventory(self, **kwargs):
        """Get fixed-term crypto-loan available inventory.

        Required args:
            currency (string): Coin name, uppercase only
            term (string): Fixed term 7: 7 days; 14: 14 days; 30: 30 days;
                90: 90 days; 180: 180 days
            annualRate (string): Customizable annual interest rate, e.g., 0.02
                means 2%

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/available-inventory
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{CryptoLoanFixed.GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY}",
            query=kwargs,
            auth=True,
        )
