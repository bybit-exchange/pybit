from enum import Enum


class Misc(str, Enum):
    GET_ANNOUNCEMENT = "/v5/announcements/index"
    REQUEST_DEMO_TRADING_FUNDS = "/v5/account/demo-apply-money"
    GET_SYSTEM_STATUS = "/v5/system/status"

    def __str__(self) -> str:
        return self.value
