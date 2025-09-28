from enum import Enum


class RateLimit(str, Enum):
    SET_API_RATE_LIMIT = "/v5/apilimit/set"
    GET_API_RATE_LIMIT = "/v5/apilimit/query"
    GET_API_RATE_LIMIT_CAP = "/v5/apilimit/query-cap"
    GET_ALL_API_RATE_LIMITS = "/v5/apilimit/query-all"

    def __str__(self) -> str:
        return self.value
