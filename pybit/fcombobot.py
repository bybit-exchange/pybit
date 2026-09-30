from enum import Enum


class FComboBot(str, Enum):
    CLOSE_COMBO_BOT = "/v5/fcombobot/close"
    CREATE_COMBO_BOT = "/v5/fcombobot/create"
    GET_COMBO_DETAIL = "/v5/fcombobot/detail"
    GET_COMBO_LIMIT = "/v5/fcombobot/getlimit"

    def __str__(self) -> str:
        return self.value
