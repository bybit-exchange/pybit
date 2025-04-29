from enum import Enum


class Broker(str, Enum):
    GET_BROKER_EARNINGS = "/v5/broker/earning-record"
    GET_EXCHANGE_BROKER_EARNINGS = "/v5/broker/earnings-info"

    def __str__(self) -> str:
        return self.value
