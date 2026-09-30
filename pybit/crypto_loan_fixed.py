from enum import Enum


class CryptoLoanFixed(str, Enum):
    GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY = "/v5/crypto-loan-fixed/available-inventory"

    def __str__(self) -> str:
        return self.value
