from enum import Enum


class RWA(str, Enum):
    GET_CONVERT_DETAIL = "/v5/rwa/stocks/convert/detail"
    GET_CONVERT_LIST = "/v5/rwa/stocks/convert/list"
    SUBMIT_CONVERT = "/v5/rwa/stocks/convert/submit"
    GET_MULTIPLIER_LIST = "/v5/rwa/stocks/market/getMultiplierList"
    GET_MARKET_SESSION = "/v5/rwa/stocks/market/session"
    PLACE_STOCKS_ORDER = "/v5/rwa/stocks/order"
    CANCEL_STOCKS_ORDER = "/v5/rwa/stocks/order/cancel"
    GET_STOCKS_ORDER_DETAIL = "/v5/rwa/stocks/order/detail"
    GET_STOCKS_POSITIONS = "/v5/rwa/stocks/positions"

    def __str__(self) -> str:
        return self.value
