from enum import Enum


class RFQ(str, Enum):
    CREATE_RFQ = "/v5/rfq/create-rfq"
    GET_CONFIG = "/v5/rfq/config"
    CANCEL_RFQ = "/v5/rfq/cancel-rfq"
    CANCEL_ALL_RFQ = "/v5/rfq/cancel-all-rfq"
    CREATE_QUOTE = "/v5/rfq/create-quote"
    EXECUTE_QUOTE = "/v5/rfq/execute-quote"
    CANCEL_QUOTE = "/v5/rfq/cancel-quote"
    CANCEL_ALL_QUOTES = "/v5/rfq/cancel-all-quotes"
    GET_RFQ_REALTIME = "/v5/rfq/rfq-realtime"
    GET_RFQ_LIST = "/v5/rfq/rfq-list"
    GET_QUOTE_REALTIME = "/v5/rfq/quote-realtime"
    GET_QUOTE_LIST = "/v5/rfq/quote-list"
    GET_TRADE_LIST = "/v5/rfq/trade-list"
    GET_PUBLIC_TRADES = "/v5/rfq/public-trades"
    ACCEPT_OTHER_QUOTE = "/v5/rfq/accept-other-quote"

    def __str__(self) -> str:
        return self.value
