from typing import DefaultDict, Any
from dataclasses import dataclass, field
import time
import hmac
import hashlib
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import json
import logging
import requests

from datetime import datetime as dt

from .exceptions import FailedRequestError, InvalidRequestError
from . import _helpers

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


def generate_signature(use_rsa_authentication, secret, param_str):
    def generate_hmac():
        hash = hmac.new(
            bytes(secret, "utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256,
        )
        return hash.hexdigest()

    def generate_rsa():
        hash = SHA256.new(param_str.encode("utf-8"))
        encoded_signature = base64.b64encode(
            PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                hash
            )
        )
        return encoded_signature.decode()

    if not use_rsa_authentication:
        return generate_hmac()
    else:
        return generate_rsa()


@dataclass
class _V5HTTPManager:
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
    retry_codes: DefaultDict[dict, Any] = field(
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
        if len(logging.root.handlers) == 0:
            # no handler on root logger set -> we add handler just for this logger to not mess with custom logic from outside
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            handler.setLevel(self.logging_level)
            self.logger.addHandler(handler)

        self.logger.debug("Initializing HTTP session.")

        self.client = requests.Session()
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        if self.referral_id:
            self.client.headers.update({"Referer": self.referral_id})

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

    def _auth(self, payload, recv_window, timestamp):
        """
        Prepares authentication signature per Bybit API specifications.
        """

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_str = str(timestamp) + self.api_key + str(recv_window) + payload

        return generate_signature(
            self.rsa_authentication, self.api_secret, param_str
        )

    @staticmethod
    def _verify_string(params, key):
        if key in params:
            if not isinstance(params[key], str):
                return False
            else:
                return True
        return True

    def _submit_request(self, method=None, path=None, query=None, auth=False):
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
        if query is not None:
            for i in query.keys():
                if isinstance(query[i], float) and query[i] == int(query[i]):
                    query[i] = int(query[i])

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

            req_params = self.prepare_payload(method, query)

            # Authenticate if we are using a private endpoint.
            if auth:
                # Prepare signature.
                timestamp = _helpers.generate_timestamp()
                signature = self._auth(
                    payload=req_params,
                    recv_window=recv_window,
                    timestamp=timestamp,
                )
                headers = {
                    "Content-Type": "application/json",
                    "X-BAPI-API-KEY": self.api_key,
                    "X-BAPI-SIGN": signature,
                    "X-BAPI-SIGN-TYPE": "2",
                    "X-BAPI-TIMESTAMP": str(timestamp),
                    "X-BAPI-RECV-WINDOW": str(recv_window),
                }
            else:
                headers = {}

            if method == "GET":
                if req_params:
                    r = self.client.prepare_request(
                        requests.Request(
                            method, path + f"?{req_params}", headers=headers
                        )
                    )
                else:
                    r = self.client.prepare_request(
                        requests.Request(method, path, headers=headers)
                    )
            else:
                r = self.client.prepare_request(
                    requests.Request(
                        method, path, data=req_params, headers=headers
                    )
                )
            
            # Log the request.
            if self.log_requests:
                if req_params:
                    self.logger.debug(
                        f"Request -> {method} {path}. Body: {req_params}. "
                        f"Headers: {r.headers}"
                    )
                else:
                    self.logger.debug(
                        f"Request -> {method} {path}. Headers: {r.headers}"
                    )

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
            if s.status_code != 200:
                if s.status_code == 403:
                    error_msg = "You have breached the IP rate limit or your IP is from the USA."
                else:
                    error_msg = "HTTP status code is not 200."
                self.logger.debug(f"Response text: {s.text}")
                raise FailedRequestError(
                    request=f"{method} {path}: {req_params}",
                    message=error_msg,
                    status_code=s.status_code,
                    time=dt.utcnow().strftime("%H:%M:%S"),
                    resp_headers=s.headers,
                )

            # Convert response to dictionary, or raise if requests error.
            try:
                s_json = s.json()

            # If we have trouble converting, handle the error and retry.
            except JSONDecodeError as e:
                if self.force_retry:
                    self.logger.error(f"{e}. {retries_remaining}")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.debug(f"Response text: {s.text}")
                    raise FailedRequestError(
                        request=f"{method} {path}: {req_params}",
                        message="Conflict. Could not decode JSON.",
                        status_code=409,
                        time=dt.utcnow().strftime("%H:%M:%S"),
                        resp_headers=s.headers,
                    )

            ret_code = "retCode"
            ret_msg = "retMsg"

            # If Bybit returns an error, raise.
            if s_json[ret_code]:
                # Generate error message.
                error_msg = f"{s_json[ret_msg]} (ErrCode: {s_json[ret_code]})"

                # Set default retry delay.
                delay_time = self.retry_delay

                # Retry non-fatal whitelisted error requests.
                if s_json[ret_code] in self.retry_codes:
                    # 10002, recv_window error; add 2.5 seconds and retry.
                    if s_json[ret_code] == 10002:
                        error_msg += ". Added 2.5 seconds to recv_window"
                        recv_window += 2500

                    # 10006, rate limit error; wait until
                    # X-Bapi-Limit-Reset-Timestamp and retry.
                    elif s_json[ret_code] == 10006:
                        self.logger.error(
                            f"{error_msg}. Hit the API rate limit. "
                            f"Sleeping, then trying again. Request: {path}"
                        )

                        # Calculate how long we need to wait in milliseconds.
                        limit_reset_time = int(s.headers["X-Bapi-Limit-Reset-Timestamp"])
                        limit_reset_str = dt.fromtimestamp(limit_reset_time / 10**3).strftime(
                            "%H:%M:%S.%f")[:-3]
                        delay_time = (int(limit_reset_time) - _helpers.generate_timestamp()) / 10**3
                        error_msg = (
                            f"API rate limit will reset at {limit_reset_str}. "
                            f"Sleeping for {int(delay_time * 10**3)} milliseconds"
                        )

                    # Log the error.
                    self.logger.error(f"{error_msg}. {retries_remaining}")
                    time.sleep(delay_time)
                    continue

                elif s_json[ret_code] in self.ignore_codes:
                    pass

                else:
                    raise InvalidRequestError(
                        request=f"{method} {path}: {req_params}",
                        message=s_json[ret_msg],
                        status_code=s_json[ret_code],
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
