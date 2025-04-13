from enum import Enum


class Earn(str, Enum):
    GET_EARN_PRODUCT_INFO = "/v5/earn/product"
    STAKE_OR_REDEEM = "/v5/earn/place-order"
    GET_STAKE_OR_REDEMPTION_HISTORY = "/v5/earn/order"
    GET_STAKED_POSITION = "/v5/earn/position"

    def __str__(self) -> str:
        return self.value
