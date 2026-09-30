from enum import Enum


class FHT(str, Enum):
    BATCH_CREATE_TAX_REPORTS = "/v5/fht/compliance/tax/private/batch_create"
    BATCH_QUERY_TAX_REPORTS = "/v5/fht/compliance/tax/private/batch_query"

    def __str__(self) -> str:
        return self.value
