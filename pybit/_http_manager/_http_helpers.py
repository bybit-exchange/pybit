import logging

from datetime import datetime as dt

from pybit import _helpers


def set_logger_handler(logger, logging_level):
    if len(logging.root.handlers) == 0:
        # no handler on root logger set -> we add handler just for this logger to not mess with custom logic from outside
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        handler.setLevel(logging_level)
        logger.addHandler(handler)


def calculate_rate_limit_delay_time(x_bapi_limit_reset_timestamp: int):
    limit_reset_str = dt.fromtimestamp(x_bapi_limit_reset_timestamp / 10 ** 3).strftime(
        "%H:%M:%S.%f")[:-3]
    delay_time = (int(x_bapi_limit_reset_timestamp) - _helpers.generate_timestamp()) / 10 ** 3
    return delay_time, limit_reset_str
