from collections import defaultdict
from dataclasses import dataclass, field
import time
import json
import logging
import requests

from datetime import datetime as dt

from pybit.exceptions import FailedRequestError, InvalidRequestError
from pybit._http_manager._auth import AuthService
from pybit._http_manager._response_handler import (
    ResponseHandler,
    ForceRetryException
)
from pybit._http_manager import _http_helpers

# Requests will use simplejson if available.
try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError

HTTP_URL = "https://{SUBDOMAIN}.{DOMAIN}.{TLD}"
SUBDOMAIN_TESTNET = "api-testnet"
SUBDOMAIN_MAINNET = "api"
DEMO_SUBDOMAIN_TESTNET = "api-demo-testnet"
DEMO_SUBDOMAIN_MAINNET = "api-demo"
DOMAIN_MAIN = "bybit"
DOMAIN_ALT = "bytick"
TLD_MAIN = "com"
TLD_NL = "nl"
TLD_HK = "com.hk"


RET_CODE = "retCode"
RET_MSG = "retMsg"


@dataclass
class _V5HTTPManager(
    AuthService,
    ResponseHandler
):
    testnet: bool = field(default=False)
    domain: str = field(default=DOMAIN_MAIN)
    tld: str = field(default=TLD_MAIN)
    demo: bool = field(default=False)
    rsa_authentication: str = field(default=False)
    api_key: str = field(default=None)
    api_secret: str = field(default=None)
    logging_level: logging = field(default=logging.INFO)
    log_requests: bool = field(default=False)
    timeout: int = field(default=10)
    recv_window: bool = field(default=5000)
    force_retry: bool = field(default=False)
    retry_codes: defaultdict[dict] = field(
        default_factory=dict,
        init=False,
    )
    ignore_codes: dict = field(
        default_factory=dict,
        init=False,
    )
    max_retries: bool = field(default=3)
    retry_delay: bool = field(default=3)
    referral_id: bool = field(default=None)
    record_request_time: bool = field(default=False)
    return_response_headers: bool = field(default=False)

    def __post_init__(self):
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        domain = DOMAIN_MAIN if not self.domain else self.domain
        if self.demo:
            if self.testnet:
                subdomain = DEMO_SUBDOMAIN_TESTNET
            else:
                subdomain = DEMO_SUBDOMAIN_MAINNET
        url = HTTP_URL.format(SUBDOMAIN=subdomain, DOMAIN=domain, TLD=self.tld)
        self.endpoint = url

        if not self.ignore_codes:
            self.ignore_codes = set()
        if not self.retry_codes:
            self.retry_codes = {10002, 10006, 30034, 30035, 130035, 130150}
        self.logger = logging.getLogger(__name__)
        _http_helpers.set_logger_handler(self.logger, self.logging_level)

        self.logger.debug("Initializing HTTP session.")

        self.client = self._init_request_client()
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        if self.referral_id:
            self.client.headers.update({"Referer": self.referral_id})

    @staticmethod
    def _init_request_client():
        return requests.Session()

    @staticmethod
    def prepare_payload(method, parameters):
        """
        Prepares the request payload and validates parameter value types.
        """

        def cast_values():
            string_params = [
                "qty",
                "price",
                "triggerPrice",
                "takeProfit",
                "stopLoss",
            ]
            integer_params = ["positionIdx"]
            for key, value in parameters.items():
                if key in string_params:
                    if type(value) != str:
                        parameters[key] = str(value)
                elif key in integer_params:
                    if type(value) != int:
                        parameters[key] = int(value)

        if method == "GET":
            payload = "&".join(
                [
                    str(k) + "=" + str(v)
                    for k, v in sorted(parameters.items())
                    if v is not None
                ]
            )
            return payload
        else:
            cast_values()
            return json.dumps(parameters)

    @staticmethod
    def _verify_string(params, key):
        if key in params:
            if not isinstance(params[key], str):
                return False
            else:
                return True
        return True

    def _log_request(self, req_params, method, path, headers):
        if self.log_requests:
            if req_params:
                self.logger.debug(
                    f"Request -> {method} {path}. Body: {req_params}. "
                    f"Headers: {headers}"
                )
            else:
                self.logger.debug(
                    f"Request -> {method} {path}. Headers: {headers}"
                )

    def _prepare_request(self, recv_window, method=None, path=None, query=None, auth=False):
        req_params = self.prepare_payload(method, query)

        # Authenticate if we are using a private endpoint.
        headers = self._prepare_auth_headers(recv_window, req_params) if auth else {}

        if method == "GET":
            path = path + f"?{req_params}" if req_params else path
            data = None
        else:
            data = req_params

        return self.client.prepare_request(
            requests.Request(method, path, data=data, headers=headers)
        )

    def _submit_request1(self, method=None, path=None, query=None, auth=False):
        """
        Submits the request to the API.

        Notes
        -------------------
        We use the params argument for the GET method, and data argument for
        the POST method. Dicts passed to the data argument must be
        JSONified prior to submitting request.

        """

        if query is None:
            query = {}

        # Store original recv_window.
        recv_window = self.recv_window

        # Bug fix: change floating whole numbers to integers to prevent
        # auth signature errors.
        self._change_floating_numbers_for_auth_signature(query)

        # Send request and return headers with body. Retry if failed.
        retries_attempted = self.max_retries
        req_params = None

        while True:
            retries_attempted -= 1
            if retries_attempted < 0:
                raise FailedRequestError(
                    request=f"{method} {path}: {req_params}",
                    message="Bad Request. Retries exceeded maximum.",
                    status_code=400,
                    time=dt.utcnow().strftime("%H:%M:%S"),
                    resp_headers=None,
                )

            retries_remaining = f"{retries_attempted} retries remain."

            r = self._prepare_request(recv_window, method, path, query, auth)

            # Log the request.
            self._log_request(self, req_params, method. path, r.headers)

            # Attempt the request.
            try:
                s = self.client.send(r, timeout=self.timeout)

            # If requests fires an error, retry.
            except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
            ) as e:
                if self.force_retry:
                    self.logger.error(f"{e}. {retries_remaining}")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise e

            # Check HTTP status code before trying to decode JSON.
            self._check_status_code(s, method, path, req_params)

            # Convert response to dictionary, or raise if requests error.
            try:
                s_json = self._convert_to_dict(s, method, path, req_params)
            except ForceRetryException as e:
                self.logger.error(f"{e}. {retries_remaining}")
                time.sleep(self.retry_delay)
                continue

            # If Bybit returns an error, raise.
            if s_json[RET_CODE]:
                # Generate error message.
                error_msg = f"{s_json[RET_MSG]} (ErrCode: {s_json[RET_CODE]})"

                # Set default retry delay.
                delay_time = self.retry_delay

                # Retry non-fatal whitelisted error requests.
                if s_json[RET_CODE] in self.retry_codes:
                    # 10002, recv_window error; add 2.5 seconds and retry.
                    if s_json[RET_CODE] == 10002:
                        error_msg += ". Added 2.5 seconds to recv_window"
                        recv_window += 2500

                    # 10006, rate limit error; wait until
                    # X-Bapi-Limit-Reset-Timestamp and retry.
                    elif s_json[RET_CODE] == 10006:
                        self.logger.error(
                            f"{error_msg}. Hit the API rate limit. "
                            f"Sleeping, then trying again. Request: {path}"
                        )

                        delay_time, limit_reset_str = _http_helpers.calculate_rate_limit_delay_time(int(s.headers["X-Bapi-Limit-Reset-Timestamp"]))
                        error_msg = (
                            f"API rate limit will reset at {limit_reset_str}. "
                            f"Sleeping for {int(delay_time * 10**3)} milliseconds"
                        )

                    # Log the error.
                    self.logger.error(f"{error_msg}. {retries_remaining}")
                    time.sleep(delay_time)
                    continue

                elif s_json[RET_CODE] in self.ignore_codes:
                    pass

                else:
                    raise InvalidRequestError(
                        request=f"{method} {path}: {req_params}",
                        message=s_json[RET_MSG],
                        status_code=s_json[RET_CODE],
                        time=dt.utcnow().strftime("%H:%M:%S"),
                        resp_headers=s.headers,
                    )
            else:
                if self.log_requests:
                    self.logger.debug(
                        f"Response headers: {s.headers}"
                    )

                if self.return_response_headers:
                    return s_json, s.elapsed, s.headers,
                elif self.record_request_time:
                    return s_json, s.elapsed
                else:
                    return s_json
