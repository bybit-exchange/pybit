from enum import Enum


class Trade(str, Enum):
    PLACE_ORDER = "/v5/order/create"
    AMEND_ORDER = "/v5/order/amend"
    CANCEL_ORDER = "/v5/order/cancel"
    GET_OPEN_ORDERS = "/v5/order/realtime"
    CANCEL_ALL_ORDERS = "/v5/order/cancel-all"
    GET_ORDER_HISTORY = "/v5/order/history"
    BATCH_PLACE_ORDER = "/v5/order/create-batch"
    BATCH_AMEND_ORDER = "/v5/order/amend-batch"
    BATCH_CANCEL_ORDER = "/v5/order/cancel-batch"
    GET_BORROW_QUOTA = "/v5/order/spot-borrow-check"
    SET_DCP = "/v5/order/disconnected-cancel-all"
    PRE_CHECK_ORDER = "/v5/order/pre-check"

    def __str__(self) -> str:
        return self.value
