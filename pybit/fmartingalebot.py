from enum import Enum


class FMartingaleBot(str, Enum):
    CLOSE_F_MART_BOT = "/v5/fmartingalebot/close"
    CREATE_F_MART_BOT = "/v5/fmartingalebot/create"
    GET_F_MART_DETAIL = "/v5/fmartingalebot/detail"
    GET_F_MART_LIMIT = "/v5/fmartingalebot/getlimit"

    def __str__(self) -> str:
        return self.value
