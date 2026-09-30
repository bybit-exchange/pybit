from enum import Enum


class DCA(str, Enum):
    CLOSE_DCA_BOT = "/v5/dca/close-bot"
    CREATE_DCA_BOT = "/v5/dca/create-bot"

    def __str__(self) -> str:
        return self.value
