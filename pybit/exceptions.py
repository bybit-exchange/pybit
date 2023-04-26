class UnauthorizedExceptionError(Exception):
    pass


class InvalidChannelTypeError(Exception):
    pass


class TopicMismatchError(Exception):
    pass


class FailedRequestError(Exception):
    """
    Exception raised for failed requests.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
    """

    def __init__(self, request, message, status_code, time, resp_headers):
        self.request = request
        self.message = message
        self.status_code = status_code
        self.time = time
        self.resp_headers = resp_headers
        super().__init__(
            f"{message.capitalize()} (ErrCode: {status_code}) (ErrTime: {time})"
            f".\nRequest → {request}."
        )


class InvalidRequestError(Exception):
    """
    Exception raised for returned Bybit errors.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
    """

    def __init__(self, request, message, status_code, time, resp_headers):
        self.request = request
        self.message = message
        self.status_code = status_code
        self.time = time
        self.resp_headers = resp_headers
        super().__init__(
            f"{message} (ErrCode: {status_code}) (ErrTime: {time})"
            f".\nRequest → {request}."
        )


class BreachedRateLimitError(FailedRequestError):
    """
    Exception raised for HTTP 403 error when breached rate limit
    """

    def __init__(self, rate_limit_reset_timestamp, **kwargs):
        super().__init__(**kwargs)

        self.rate_limit_reset_timestamp = rate_limit_reset_timestamp
