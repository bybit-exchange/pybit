from enum import Enum


class Grid(str, Enum):
    CLOSE_GRID_BOT = "/v5/grid/close-grid"
    CREATE_GRID_BOT = "/v5/grid/create-grid"
    QUERY_GRID_DETAIL = "/v5/grid/query-grid-detail"
    VALIDATE_GRID_INPUT = "/v5/grid/validate-input"

    def __str__(self) -> str:
        return self.value
