from enum import Enum


class CryptoLoanFlexible(str, Enum):
    GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY = "/v5/crypto-loan-flexible/available-inventory"

    def __str__(self) -> str:
        return self.value
