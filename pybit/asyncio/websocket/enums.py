from enum import Enum


class WSState(Enum):
    INITIALISING = "Initialising"
    STREAMING = "Streaming"
    RECONNECTING = "Reconnecting"
    EXITING = "Exiting"
    FAILED = "Failed"
