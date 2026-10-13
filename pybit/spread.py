from enum import Enum


class Spread(str, Enum):
    GET_INSTRUMENTS_INFO = "/v5/spread/instrument"
    GET_ORDERBOOK = "/v5/spread/orderbook"
    GET_TICKERS = "/v5/spread/tickers"
    GET_PUBLIC_TRADING_HISTORY = "/v5/spread/recent-trade"
    PLACE_ORDER = "/v5/spread/order/create"
    AMEND_ORDER = "/v5/spread/order/amend"
    CANCEL_ORDER = "/v5/spread/order/cancel"
    CANCEL_ALL_ORDERS = "/v5/spread/order/cancel-all"
    GET_OPEN_ORDERS = "/v5/spread/order/realtime"
    GET_ORDER_HISTORY = "/v5/spread/order/history"
    GET_TRADE_HISTORY = "/v5/spread/execution/list"

    GET_SPREAD_MAX_QTY = "/v5/spread/max-qty"
    def __str__(self) -> str:
        return self.value
