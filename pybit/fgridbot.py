from enum import Enum


class FGridBot(str, Enum):
    CLOSE_F_GRID_BOT = "/v5/fgridbot/close"
    CREATE_F_GRID_BOT = "/v5/fgridbot/create"
    GET_F_GRID_DETAIL = "/v5/fgridbot/detail"
    VALIDATE_F_GRID_INPUT = "/v5/fgridbot/validate"

    def __str__(self) -> str:
        return self.value
