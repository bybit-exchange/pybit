import asyncio
import logging
import time
from json import JSONDecodeError
from typing import Optional
from datetime import (
    datetime as dt,
    timezone
)

import aiohttp

from pybit import _http_manager
from pybit import _helpers
from pybit.exceptions import (
    FailedRequestError,
    InvalidRequestError,
)
from pybit.asyncio.utils import get_event_loop
from pybit.asyncio.builder import RequestBuilder


class AsyncClient:
    def __init__(
            self,
            testnet: bool = False,
            domain: str = _http_manager.DOMAIN_MAIN,
            tld: str = _http_manager.TLD_MAIN,
            demo: bool = False,
            rsa_authentication: bool = False,
            api_key: str = None,
            api_secret: str = None,
            logging_level: int = logging.INFO,
            log_requests: bool = False,
            timeout: int = 10,
            recv_window: int = 5000,
            force_retry: bool = False,
            retry_codes: set = None,
            ignore_codes: set = None,
            max_retries: int = 3,
            retry_delay: int = 3,
            referral_id: str = None,
            record_request_time: bool = False,
            return_response_headers: bool = False,
            loop: asyncio.AbstractEventLoop = None,
            proxy: Optional[str] = None
    ):
        self.testnet = testnet
        self.domain = domain
        self.tld = tld
        self.demo = demo
        self.rsa_authentication = rsa_authentication
        self.api_key = api_key
        self.api_secret = api_secret
        self.logging_level = logging_level
        self.log_requests = log_requests
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.recv_window = recv_window
        self.force_retry = force_retry
        self.retry_codes = retry_codes or {}
        self.ignore_codes = ignore_codes or {10002, 10006, 30034, 30035, 130035, 130150}
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.referral_id = referral_id
        self.record_request_time = record_request_time
        self.return_response_headers = return_response_headers
        self._loop = loop or get_event_loop()
        self._proxy = proxy

        subdomain = _http_manager.SUBDOMAIN_TESTNET if self.testnet else _http_manager.SUBDOMAIN_MAINNET
        domain = _http_manager.DOMAIN_MAIN if not self.domain else self.domain
        if self.demo:
            if self.testnet:
                subdomain = _http_manager.DEMO_SUBDOMAIN_TESTNET
            else:
                subdomain = _http_manager.DEMO_SUBDOMAIN_MAINNET
        url = _http_manager.HTTP_URL.format(SUBDOMAIN=subdomain, DOMAIN=domain, TLD=self.tld)
        self.endpoint = url
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
        self._session = None
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.referral_id:
            self._headers['Referer'] = self.referral_id

        self._request_builder = RequestBuilder(
            api_key=self.api_key,
            api_secret=self.api_secret,
            rsa_authentication=self.rsa_authentication,
            proxy=self._proxy
        )

    async def __aenter__(self):
        await self.init_client()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close_connection()

    async def init_client(self):
        self._session = aiohttp.ClientSession(
            headers=self._headers,
            loop=self._loop,
            timeout=self.timeout
        )

    async def close_connection(self):
        await self._session.close()

    async def _submit_request(self, method: str, path: str, auth: bool = False, query: Optional[dict] = None):
        query = self._request_builder.clean_query(query)
        recv_window = self.recv_window
        retries_attempted = self.max_retries
        req_params = None

        while retries_attempted > 0:
            retries_attempted -= 1
            try:
                req_params = self._request_builder.prepare_payload(method, query)
                headers = self._request_builder.prepare_headers(req_params, recv_window) if auth else {}
                _request = self._request_builder.prepare_request(method, path, headers, req_params)
                self._log_request(method, path, req_params, headers)

                start_time = time.perf_counter()
                async with getattr(self._session, method.lower())(**_request) as response:
                    end_time = time.perf_counter()
                    await self._check_status_code(response, method, path, req_params)
                    return await self._handle_response(
                        response, method, path, req_params, recv_window, end_time - start_time
                    )

            except (
                aiohttp.ClientSSLError,
                aiohttp.ClientResponseError,
                aiohttp.ClientConnectionError,
                asyncio.exceptions.TimeoutError
            ) as e:
                await self._handle_network_error(e, retries_attempted)
            except (JSONDecodeError, aiohttp.ContentTypeError) as e:
                await self._handle_json_error(e, retries_attempted)

        raise FailedRequestError(
            request=f"{method} {path}: {req_params or query}",
            message="Bad Request. Retries exceeded maximum.",
            status_code=400,
            time=dt.now(timezone.utc).strftime("%H:%M:%S"),
            resp_headers=None,
        )

    async def _check_status_code(
            self,
            response: aiohttp.ClientResponse,
            method: str,
            path: str,
            params: str
    ):
        """Check HTTP status code."""
        if response.status != 200:
            error_msg = "You have breached the IP rate limit or your IP is from the USA." \
                if response.status == 403 else "HTTP status code is not 200."
            self.logger.debug(f"Response text: {await response.text()}")
            raise FailedRequestError(
                request=f"{method} {path}: {params}",
                message=error_msg,
                status_code=response.status,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

    async def _handle_response(
            self,
            response: aiohttp.ClientResponse,
            method: str,
            path: str,
            params: str,
            recv_window: int,
            response_time: float
    ):
        try:
            s_json = await response.json()
        except (JSONDecodeError, aiohttp.ContentTypeError) as e:
            raise e  # Will be caught by main loop to retry.

        ret_code = "retCode"
        ret_msg = "retMsg"

        if s_json.get(ret_code):
            error_code = s_json[ret_code]
            error_msg = f"{s_json[ret_msg]} (ErrCode: {error_code})"

            if error_code in self.retry_codes:
                await self._handle_retryable_error(response, error_code, error_msg, recv_window)
                raise Exception("Retryable error occurred, retrying...")

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
            return s_json, response_time, response.headers
        elif self.record_request_time:
            return s_json, response_time
        else:
            return s_json

    def _log_request(self, method, path, params, headers):
        """Log request."""
        if self.log_requests:
            if params:
                self.logger.debug(f"Request -> {method} {path}. Body: {params}. Headers: {headers}")
            else:
                self.logger.debug(f"Request -> {method} {path}. Headers: {headers}")

    async def _handle_retryable_error(self, response, error_code, error_msg, recv_window):
        """Handle specific retryable Bybit errors."""
        delay_time = self.retry_delay

        if error_code == 10002:  # recv_window error
            error_msg += ". Added 2.5 seconds to recv_window"
            recv_window += 2500
        elif error_code == 10006:  # rate limit error
            self.logger.error(f"{error_msg}. Hit the API rate limit on {response.url}. Sleeping then trying again.")
            limit_reset_time = int(response.headers["X-Bapi-Limit-Reset-Timestamp"])
            limit_reset_str = dt.fromtimestamp(limit_reset_time / 10 ** 3).strftime("%H:%M:%S.%f")[:-3]
            delay_time = (limit_reset_time - _helpers.generate_timestamp()) / 10 ** 3
            error_msg = f"API rate limit will reset at {limit_reset_str}. Sleeping for {int(delay_time * 10 ** 3)} ms"

        self.logger.error(f"{error_msg}. Retrying...")
        await asyncio.sleep(delay_time)

    async def _handle_network_error(self, error, retries_attempted):
        """Handle network-related exceptions."""
        if self.force_retry and retries_attempted > 0:
            self.logger.error(f"{error}. Retrying...")
            await asyncio.sleep(self.retry_delay)
        else:
            raise error

    async def _handle_json_error(self, error, retries_attempted):
        """Handle JSON decoding errors."""
        if self.force_retry and retries_attempted > 0:
            self.logger.error(f"{error}. Retrying JSON decode...")
            await asyncio.sleep(self.retry_delay)
        else:
            raise FailedRequestError(
                request="JSON decoding",
                message="Conflict. Could not decode JSON.",
                status_code=409,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=None,
            )
