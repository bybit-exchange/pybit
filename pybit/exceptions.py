
""" This module contains the exceptions for the Pybit package. """

from ._utils import deprecate_class


class PybitException(Exception):
    """
    Base exception class for all exceptions.
    """


class WSConnectionNotEstablishedException(PybitException):
    """
    Exception raised when connection is not established.
    """

    def __init__(self):
        super().__init__("WebSocket connection is not established. Please connect first.")


# =================== Authorization Exceptions ===================
class AuthorizationException(PybitException):
    """
    Base exception class for all authorization exceptions.
    """


@deprecate_class(
    '6.0',
    replacement='NoCredentialsAuthorizationException',
)
class UnauthorizedExceptionError(AuthorizationException):
    """
    Exception raised for unauthorized requests.
    """


class NoCredentialsAuthorizationException(UnauthorizedExceptionError):
    """
    Exception raised when no credentials are provided.
    """

    def __init__(self):
        super().__init__('"api_key" and/or "api_secret" are not set. They both are needed in order to access private sources')


class AuthorizationFailedException(AuthorizationException):
    """
    Exception raised when authorization fails.
    """

    def __init__(self, ws_name: str, raw_message: str):
        super().__init__(
            f"Authorization for {ws_name} failed. Please check your "
            f"API keys and resync your system time. Raw error: {raw_message}"
        )
# ===============================================================


@deprecate_class(
    '6.0',
    replacement='InvalidChannelTypeException',
)
class InvalidChannelTypeError(PybitException):
    """
    Exception raised for invalid channel types.
    """


class InvalidChannelTypeException(InvalidChannelTypeError):
    """
    Exception raised for invalid channel types.
    """

    def __init__(self, provided_channel: str, available_channels: list[str]):
        super().__init__(
            f'Invalid channel type("{provided_channel}"). Available: {available_channels}')


# ================ Topic Exceptions ========================
class TopicException(PybitException):
    """
    Base exception class for all topic exceptions.
    """


@deprecate_class(
    '6.0',
    replacement='TopicMismatchException',
)
class TopicMismatchError(TopicException):
    """
    Exception raised for topic mismatch.
    """


class TopicMismatchException(TopicMismatchError):
    """
    Exception raised for topic mismatch.
    """

    def __init__(self):
        super().__init__("Requested topic does not match channel_type")


class AlreadySubscribedTopicException(TopicException):
    """
    Exception raised for already subscribed topics.
    """

    def __init__(self, topic: str):
        super().__init__(f"Already subscribed to topic: {topic}")
# ============================================================


@deprecate_class(
    '6.0',
    replacement='FailedRequestException',
)
class FailedRequestError(PybitException):
    # TODO: Remove this class in the next major release
    # and copy-paste the __init__ method from this class to the replacement class
    """
    Exception raised for failed requests.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
        resp_headers -- The response headers from API. None, if the request caused an error locally.
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


class FailedRequestException(FailedRequestError):
    """
    Exception raised for failed requests.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
        resp_headers -- The response headers from API. None, if the request caused an error locally.
    """


@deprecate_class(
    '6.0',
    replacement='InvalidRequestException',
)
class InvalidRequestError(PybitException):
    # TODO: Remove this class in the next major release
    # and copy-paste the __init__ method from this class to the replacement class
    """
    Exception raised for returned Bybit errors.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
        resp_headers -- The response headers from API. None, if the request caused an error locally.
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


class InvalidRequestException(FailedRequestError):
    """
    Exception raised for returned Bybit errors.

    Attributes:
        request -- The original request that caused the error.
        message -- Explanation of the error.
        status_code -- The code number returned.
        time -- The time of the error.
        resp_headers -- The response headers from API. None, if the request caused an error locally.
    """
