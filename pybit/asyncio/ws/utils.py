from random import random
from typing import Iterable


def get_reconnect_wait(attempts: int) -> int:
    expo = 2 ** attempts
    # 900 - is max reconnect seconds
    return round(random() * min(900, expo - 1) + 1)


def chunks(lst: list, n: int) -> Iterable:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
