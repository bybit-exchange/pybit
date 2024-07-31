import logging
from json import JSONDecodeError
from dataclasses import dataclass, field

from datetime import datetime as dt

from pybit.exceptions import FailedRequestError
from pybit._http_manager._http_helpers import set_logger_handler


class ForceRetryException(Exception): ...


@dataclass
class ResponseHandler:
    logging_level: logging = field(default=logging.INFO)
    force_retry: bool = field(default=False)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        set_logger_handler(self.logger, self.logging_level)

        self.logger.debug("Initializing HTTP session.")

    def _check_status_code(self, response, method, path, req_params):
        if response.status_code != 200:
            if response.status_code == 403:
                error_msg = "You have breached the IP rate limit or your IP is from the USA."
            else:
                error_msg = "HTTP status code is not 200."
            self.logger.debug(f"Response text: {response.text}")
            raise FailedRequestError(
                request=f"{method} {path}: {req_params}",
                message=error_msg,
                status_code=response.status_code,
                time=dt.utcnow().strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

    def _convert_to_dict(self, response, method, path, req_params):
        try:
            return response.json()
        # If we have trouble converting, handle the error and retry.
        except JSONDecodeError as e:
            if self.force_retry:
                raise ForceRetryException(str(e))
            else:
                self.logger.debug(f"Response text: {response.text}")
                raise FailedRequestError(
                    request=f"{method} {path}: {req_params}",
                    message="Conflict. Could not decode JSON.",
                    status_code=409,
                    time=dt.utcnow().strftime("%H:%M:%S"),
                    resp_headers=response.headers,
                )
