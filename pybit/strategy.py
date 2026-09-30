from enum import Enum


class Strategy(str, Enum):
    CREATE_CHASE_ORDER_STRATEGY = "/v5/strategy/create"
    QUERY_STRATEGY_LIST = "/v5/strategy/list"
    QUERY_STRATEGY_ORDER_LIST = "/v5/strategy/order-list"
    STOP_STRATEGY = "/v5/strategy/stop"

    def __str__(self) -> str:
        return self.value
