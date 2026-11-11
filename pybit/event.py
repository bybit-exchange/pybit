from enum import Enum


class Event(str, Enum):
    GET_EC_ORDER_HISTORY = "/v5/event/order-list"
    GET_EC_ACTIVE_ORDERS = "/v5/event/order-realtime"
    GET_EC_POSITION_INFO = "/v5/event/positions"
    GET_EC_SETTLEMENTS = "/v5/event/settlements"
    GET_EC_TRADE_HISTORY = "/v5/event/trades"

    def __str__(self) -> str:
        return self.value
