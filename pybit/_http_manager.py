from collections import defaultdict
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
import os
import requests

from datetime import datetime as dt, timezone

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
DOMAIN_TK = "bybit-tr"  # Turkey
TLD_MAIN = "com"        # Global
TLD_NL = "nl"           # The Netherlands
TLD_HK = "com.hk"       # Hong Kong
TLD_KZ = "kz"           # Kazakhstan
TLD_EU = "eu"           # European Economic Area. ONLY AVAILABLE TO INSTITUTIONS


class _RetryableRequestError(Exception):
    def __init__(self, recv_window):
        self.recv_window = recv_window
        super().__init__("Retryable error occurred, retrying...")


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


def generate_signature_binary(use_rsa_authentication, secret, param_bytes):
    def generate_hmac():
        hash = hmac.new(
            bytes(secret, "utf-8"),
            param_bytes,
            hashlib.sha256,
        )
        return hash.hexdigest()

    def generate_rsa():
        hash = SHA256.new(param_bytes)
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
    retry_codes: defaultdict[dict] = field(default_factory=dict)
    ignore_codes: set = field(default_factory=set)
    max_retries: bool = field(default=3)
    retry_delay: bool = field(default=3)
    referral_id: str = field(default=None)
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
            # no handler on root logger set -> we add handler just for this logger to not mess with custom logic from
            # outside
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

    def _auth_binary(self, payload, recv_window, timestamp):
        """
        Prepares authentication signature for binary request bodies.
        """

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_bytes = (
            str(timestamp) + self.api_key + str(recv_window)
        ).encode("utf-8") + payload

        return generate_signature_binary(
            self.rsa_authentication, self.api_secret, param_bytes
        )

    def _submit_request(self, method=None, path=None, query=None, auth=False):
        """
        Submits the request to the API.
        """
        query = self._clean_query(query)
        recv_window = self.recv_window
        retries_attempted = self.max_retries

        while retries_attempted > 0:
            retries_attempted -= 1
            try:
                req_params = self.prepare_payload(method, query)
                headers = self._prepare_headers(req_params, recv_window) if auth else {}

                request = self._prepare_request(method, path, req_params, headers)
                self._log_request(method, path, req_params, request.headers)

                response = self.client.send(request, timeout=self.timeout)
                self._check_status_code(response, method, path, req_params)

                return self._handle_response(response, method, path, req_params, recv_window, retries_attempted)

            except _RetryableRequestError as e:
                recv_window = e.recv_window
                continue
            except (requests.exceptions.ReadTimeout, requests.exceptions.SSLError,
                    requests.exceptions.ConnectionError) as e:
                self._handle_network_error(e, retries_attempted)
            except JSONDecodeError as e:
                self._handle_json_error(e, retries_attempted)

        raise FailedRequestError(
            request=f"{method} {path}: {req_params}",
            message="Bad Request. Retries exceeded maximum.",
            status_code=400,
            time=dt.now(timezone.utc).strftime("%H:%M:%S"),
            resp_headers=None,
        )

    def _submit_file_request(self, path=None, query=None, auth=True):
        """
        Submits an authenticated multipart file request to the API.
        """
        query = self._clean_query(query)
        recv_window = self.recv_window
        retries_attempted = self.max_retries

        while retries_attempted > 0:
            retries_attempted -= 1
            try:
                req_params, content_type = self.prepare_file_payload(query)
                headers = (
                    self._prepare_headers(
                        req_params,
                        recv_window,
                        content_type=content_type,
                    )
                    if auth else {}
                )

                request = self._prepare_request(
                    "POST",
                    path,
                    req_params,
                    headers,
                )
                self._log_request("POST", path, "<binary payload>", request.headers)

                response = self.client.send(request, timeout=self.timeout)
                self._check_status_code(
                    response,
                    "POST",
                    path,
                    "<binary payload>",
                )

                return self._handle_response(
                    response,
                    "POST",
                    path,
                    "<binary payload>",
                    recv_window,
                    retries_attempted,
                )

            except _RetryableRequestError as e:
                recv_window = e.recv_window
                continue
            except (requests.exceptions.ReadTimeout, requests.exceptions.SSLError,
                    requests.exceptions.ConnectionError) as e:
                self._handle_network_error(e, retries_attempted)
            except JSONDecodeError as e:
                self._handle_json_error(e, retries_attempted)

        raise FailedRequestError(
            request=f"POST {path}: <binary payload>",
            message="Bad Request. Retries exceeded maximum.",
            status_code=400,
            time=dt.now(timezone.utc).strftime("%H:%M:%S"),
            resp_headers=None,
        )

    def _clean_query(self, query):
        """Remove None values and fix floats."""
        if query is None:
            return {}
        for key in list(query.keys()):
            if isinstance(query[key], float) and query[key] == int(query[key]):
                query[key] = int(query[key])
        return {k: v for k, v in query.items() if v is not None}

    def _prepare_headers(self, payload, recv_window, content_type="application/json"):
        """Prepare headers for authenticated request."""
        timestamp = _helpers.generate_timestamp()
        if isinstance(payload, bytes):
            signature = self._auth_binary(
                payload=payload,
                recv_window=recv_window,
                timestamp=timestamp,
            )
        else:
            signature = self._auth(
                payload=payload,
                recv_window=recv_window,
                timestamp=timestamp,
            )
        return {
            "Content-Type": content_type,
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": str(timestamp),
            "X-BAPI-RECV-WINDOW": str(recv_window),
        }

    @staticmethod
    def _normalize_upload_input(upload_file, filename=None):
        if isinstance(upload_file, (bytes, bytearray, memoryview)):
            if not filename:
                raise ValueError("filename is required when passing raw bytes.")
            return bytes(upload_file), filename

        if isinstance(upload_file, (str, os.PathLike)):
            path = os.fspath(upload_file)
            with open(path, "rb") as file:
                return file.read(), filename or os.path.basename(path)

        if hasattr(upload_file, "read"):
            position = None
            if hasattr(upload_file, "tell") and hasattr(upload_file, "seek"):
                try:
                    position = upload_file.tell()
                except Exception:
                    position = None

            data = upload_file.read()
            if position is not None:
                try:
                    upload_file.seek(position)
                except Exception:
                    pass

            filename = filename or getattr(upload_file, "name", None)
            if not filename:
                raise ValueError(
                    "filename is required when passing a file-like without name."
                )
            if isinstance(data, str):
                data = data.encode("utf-8")
            return data, os.path.basename(str(filename))

        raise TypeError(f"Unsupported upload_file type: {type(upload_file)!r}")

    @classmethod
    def prepare_file_payload(cls, parameters):
        """
        Prepares multipart payload for authenticated file uploads.
        """
        if "upload_file" not in parameters:
            raise ValueError("Missing required parameter: upload_file")

        data, filename = cls._normalize_upload_input(
            parameters["upload_file"],
            filename=parameters.get("filename"),
        )
        boundary = "boundary-for-file"
        content_type = f"multipart/form-data; boundary={boundary}"
        body = b"".join(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    'Content-Disposition: form-data; name="upload_file"; '
                    f'filename="{filename}"\r\n'
                ).encode("utf-8"),
                b"Content-Type: image/png\r\n\r\n",
                data,
                f"\r\n--{boundary}--\r\n".encode("utf-8"),
            ]
        )
        return body, content_type

    def _prepare_request(self, method, path, params, headers):
        """Prepare request object."""
        if method == "GET" and params:
            return self.client.prepare_request(requests.Request(method, f"{path}?{params}", headers=headers))
        return self.client.prepare_request(requests.Request(method, path, data=params, headers=headers))

    def _log_request(self, method, path, params, headers):
        """Log request."""
        if self.log_requests:
            if params:
                self.logger.debug(f"Request -> {method} {path}. Body: {params}. Headers: {headers}")
            else:
                self.logger.debug(f"Request -> {method} {path}. Headers: {headers}")

    def _check_status_code(self, response, method, path, params):
        """Check HTTP status code."""
        if response.status_code != 200:
            error_msg = "You have breached the IP rate limit or your IP is from the USA."\
                if response.status_code == 403 else "HTTP status code is not 200."
            self.logger.debug(f"Response text: {response.text}")
            raise FailedRequestError(
                request=f"{method} {path}: {params}",
                message=error_msg,
                status_code=response.status_code,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

    def _handle_response(self, response, method, path, params, recv_window, retries_attempted):
        """Handle JSON response and Bybit error codes."""
        try:
            s_json = response.json()
        except JSONDecodeError as e:
            raise e  # Will be caught by main loop to retry.

        ret_code = "retCode" if "retCode" in s_json else "ret_code"
        ret_msg = "retMsg" if "retMsg" in s_json else "ret_msg"

        if s_json.get(ret_code):
            error_code = s_json[ret_code]
            error_msg = f"{s_json[ret_msg]} (ErrCode: {error_code})"

            if error_code in self.retry_codes:
                recv_window = self._handle_retryable_error(
                    response, error_code, error_msg, recv_window
                )
                raise _RetryableRequestError(recv_window)

            if error_code not in self.ignore_codes:
                raise InvalidRequestError(
                    request=f"{method} {path}: {params}",
                    message=s_json[ret_msg],
                    status_code=error_code,
                    time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                    resp_headers=response.headers,
                )

        if self.log_requests:
            self.logger.debug(f"Response headers: {response.headers}")

        if self.return_response_headers:
            return s_json, response.elapsed, response.headers
        elif self.record_request_time:
            return s_json, response.elapsed
        else:
            return s_json

    def _handle_retryable_error(self, response, error_code, error_msg, recv_window):
        """Handle specific retryable Bybit errors."""
        delay_time = self.retry_delay

        if error_code == 10002:  # recv_window error
            error_msg += ". Added 2.5 seconds to recv_window"
            recv_window += 2500
        elif error_code == 10006:  # rate limit error
            self.logger.error(f"{error_msg}. Hit the API rate limit on {response.url}. Sleeping then trying again.")
            limit_reset_time = int(
                response.headers.get(
                    "X-Bapi-Limit-Reset-Timestamp",
                    _helpers.generate_timestamp() + 2000
                )
            )
            limit_reset_str = dt.fromtimestamp(limit_reset_time / 10 ** 3).strftime("%H:%M:%S.%f")[:-3]
            delay_time = (limit_reset_time - _helpers.generate_timestamp()) / 10 ** 3
            error_msg = f"API rate limit will reset at {limit_reset_str}. Sleeping for {int(delay_time * 10 ** 3)} ms"

        self.logger.error(f"{error_msg}. Retrying...")
        time.sleep(delay_time)
        return recv_window

    def _handle_network_error(self, error, retries_attempted):
        """Handle network-related exceptions."""
        if self.force_retry and retries_attempted > 0:
            self.logger.error(f"{error}. Retrying...")
            time.sleep(self.retry_delay)
        else:
            raise error

    def _handle_json_error(self, error, retries_attempted):
        """Handle JSON decoding errors."""
        if self.force_retry and retries_attempted > 0:
            self.logger.error(f"{error}. Retrying JSON decode...")
            time.sleep(self.retry_delay)
        else:
            raise FailedRequestError(
                request="JSON decoding",
                message="Conflict. Could not decode JSON.",
                status_code=409,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=None,
            )
