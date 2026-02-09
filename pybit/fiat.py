from enum import Enum


class Fiat(str, Enum):
    GET_COIN_LIST = "/v5/fiat/query-coin-list"
    GET_REFERENCE_PRICE = "/v5/fiat/reference-price"
    REQUEST_QUOTE = "/v5/fiat/quote-apply"
    EXECUTE_TRADE = "/v5/fiat/trade-execute"
    QUERY_TRADE = "/v5/fiat/trade-query"
    GET_TRADE_HISTORY = "/v5/fiat/query-trade-history"
    GET_BALANCE = "/v5/fiat/balance-query"

    def __str__(self) -> str:
        return self.value
