import asyncio
import logging
import time
from json import JSONDecodeError
from typing import Optional, Set
from datetime import (
    datetime as dt,
    timedelta,
    timezone,
)

import aiohttp

from pybit import _http_manager
from pybit import _helpers
from pybit._http_manager import _RetryableRequestError
from pybit.exceptions import (
    FailedRequestError,
    InvalidRequestError,
)
from pybit.asyncio.builder import RequestBuilder

# Library-level NullHandler — the application is responsible for configuring
# logging output; we only need to prevent the "no handlers" warning.
logging.getLogger(__name__).addHandler(logging.NullHandler())


class AsyncClient:
    def __init__(
            self,
            testnet: bool = False,
            domain: str = _http_manager.DOMAIN_MAIN,
            tld: str = _http_manager.TLD_MAIN,
            demo: bool = False,
            rsa_authentication: bool = False,
            api_key: Optional[str] = None,
            api_secret: Optional[str] = None,
            logging_level: int = logging.INFO,
            log_requests: bool = False,
            timeout: int = 10,
            recv_window: int = 5000,
            force_retry: bool = False,
            retry_codes: Optional[Set[int]] = None,
            ignore_codes: Optional[Set[int]] = None,
            max_retries: int = 3,
            retry_delay: int = 3,
            referral_id: Optional[str] = None,
            record_request_time: bool = False,
            return_response_headers: bool = False,
            proxy: Optional[str] = None,
            trace_configs: Optional[list] = None,
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
        # `is not None` so an explicit empty set is respected.
        self.retry_codes = (
            retry_codes if retry_codes is not None
            else {10002, 10006, 30034, 30035, 130035, 130150}
        )
        self.ignore_codes = ignore_codes if ignore_codes is not None else set()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.referral_id = referral_id
        self.record_request_time = record_request_time
        self.return_response_headers = return_response_headers
        self._proxy = proxy
        self._trace_configs = trace_configs
        # In-flight guard: set when close_connection starts so a concurrent
        # ``_submit_request`` (esp. one that force-retries) doesn't race into
        # ``getattr(None, method)`` after ``self._session`` has been cleared.
        self._closed = False

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
        # PEP 282: libraries should not attach stream handlers — that
        # duplicates output for any app that uses ``logging.basicConfig()``.
        # We add a NullHandler once (module-level below) so the "No handlers
        # could be found" warning never fires; the application decides where
        # logs go. ``logging_level`` still works via ``self.logger.setLevel``.
        self.logger.setLevel(self.logging_level)
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
            proxy=self._proxy,
        )

    async def __aenter__(self):
        await self.init_client()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close_connection()

    async def init_client(self):
        """Create the aiohttp session. Must be called from within a running
        event loop (``async with`` handles this automatically)."""
        if self._closed:
            raise RuntimeError("AsyncClient has been closed; create a new instance")
        if self._session is not None:
            return
        session_kwargs = {
            "headers": self._headers,
            "timeout": self.timeout,
        }
        if self._trace_configs:
            session_kwargs["trace_configs"] = self._trace_configs
        self._session = aiohttp.ClientSession(**session_kwargs)

    async def close_connection(self):
        self._closed = True
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _submit_request(
            self,
            method: str,
            path: str,
            auth: bool = False,
            query: Optional[dict] = None,
    ):
        if self._closed:
            raise FailedRequestError(
                request=f"{method} {path}",
                message="AsyncClient is closed",
                status_code=0,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=None,
            )
        if self._session is None:
            await self.init_client()

        query = self._request_builder.clean_query(query)
        recv_window = self.recv_window
        retries_attempted = self.max_retries
        req_params = None
        last_exc: Optional[BaseException] = None
        last_retry_reason: Optional[str] = None

        while retries_attempted > 0:
            retries_attempted -= 1
            # Re-check on each iteration so an in-flight retry loop bails out
            # promptly when close_connection() runs mid-request.
            if self._closed:
                raise FailedRequestError(
                    request=f"{method} {path}",
                    message="AsyncClient is closed",
                    status_code=0,
                    time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                    resp_headers=None,
                )
            try:
                req_params = self._request_builder.prepare_payload(method, query)
                headers = (
                    self._request_builder.prepare_headers(req_params, recv_window)
                    if auth else {}
                )
                _request = self._request_builder.prepare_request(
                    method, path, headers, req_params
                )
                self._log_request(method, path, req_params, headers)

                start_time = time.perf_counter()
                async with getattr(self._session, method.lower())(**_request) as response:
                    await self._check_status_code(response, method, path, req_params)
                    result = await self._handle_response(
                        response, method, path, req_params, recv_window, start_time
                    )
                    return result

            except _RetryableRequestError as e:
                recv_window = e.recv_window
                # Preserve retCode/retMsg from the last retryable response so
                # that a retries-exhausted FailedRequestError carries a useful
                # message instead of the generic "Bad Request".
                last_retry_reason = e.reason
                continue
            except (
                aiohttp.ClientSSLError,
                aiohttp.ClientResponseError,
                aiohttp.ClientConnectionError,
                asyncio.TimeoutError,
            ) as e:
                last_exc = e
                await self._handle_network_error(e, retries_attempted)
            except (JSONDecodeError, aiohttp.ContentTypeError) as e:
                last_exc = e
                await self._handle_json_error(e, retries_attempted)

        message = (
            f"Retries exceeded maximum ({self.max_retries}). "
            f"Last retryable error: {last_retry_reason}"
            if last_retry_reason
            else "Bad Request. Retries exceeded maximum."
        )
        raise FailedRequestError(
            request=f"{method} {path}: {req_params or query}",
            message=message,
            status_code=400,
            time=dt.now(timezone.utc).strftime("%H:%M:%S"),
            resp_headers=None,
        ) from last_exc

    async def _check_status_code(
            self,
            response: aiohttp.ClientResponse,
            method: str,
            path: str,
            params: str,
    ):
        """Check HTTP status code."""
        if response.status != 200:
            error_msg = (
                "You have breached the IP rate limit or your IP is from the USA."
                if response.status == 403 else "HTTP status code is not 200."
            )
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
            start_time: float,
    ):
        try:
            s_json = await response.json()
        except (JSONDecodeError, aiohttp.ContentTypeError) as e:
            raise e  # Will be caught by main loop to retry.

        # Measure elapsed after the body is read (sync's ``response.elapsed``
        # includes body-read time; matching that keeps latency observability
        # meaningful for large payloads).
        elapsed = timedelta(seconds=time.perf_counter() - start_time)

        # Prefer v5 ``retCode`` / ``retMsg`` but fall back to the legacy
        # ``ret_code`` / ``ret_msg`` shape used by some P2P/OTC endpoints —
        # otherwise a non-zero legacy error would be silently dropped and
        # returned to the caller as "success".
        error_code = s_json.get("retCode")
        if error_code is None:
            error_code = s_json.get("ret_code")
        if error_code:
            ret_msg = s_json.get("retMsg", s_json.get("ret_msg", ""))
            error_msg = f"{ret_msg} (ErrCode: {error_code})"

            if error_code in self.retry_codes:
                new_recv_window = await self._handle_retryable_error(
                    response, error_code, error_msg, recv_window
                )
                raise _RetryableRequestError(new_recv_window, reason=error_msg)

            if error_code not in self.ignore_codes:
                raise InvalidRequestError(
                    request=f"{method} {path}: {params}",
                    message=ret_msg,
                    status_code=error_code,
                    time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                    resp_headers=response.headers,
                )

        if self.log_requests:
            self.logger.debug(f"Response headers: {response.headers}")

        if self.return_response_headers:
            return s_json, elapsed, response.headers
        elif self.record_request_time:
            return s_json, elapsed
        else:
            return s_json

    def _log_request(self, method, path, params, headers):
        """Log request; API key and signature are redacted so log aggregators
        (Datadog / ELK / CloudWatch) don't collect credentials from any
        debug-level line."""
        if not self.log_requests:
            return
        redacted = dict(headers)
        for sensitive in ("X-BAPI-API-KEY", "X-BAPI-SIGN"):
            if sensitive in redacted:
                redacted[sensitive] = "***REDACTED***"
        if params:
            self.logger.debug(f"Request -> {method} {path}. Body: {params}. Headers: {redacted}")
        else:
            self.logger.debug(f"Request -> {method} {path}. Headers: {redacted}")

    async def _handle_retryable_error(self, response, error_code, error_msg, recv_window):
        """Handle specific retryable Bybit errors. Returns the (possibly updated) recv_window."""
        delay_time = self.retry_delay

        if error_code == 10002:  # recv_window error
            error_msg += ". Added 2.5 seconds to recv_window"
            recv_window += 2500
        elif error_code == 10006:  # rate limit
            self.logger.error(
                f"{error_msg}. Hit the API rate limit on {response.url}. Sleeping then trying again."
            )
            raw_reset = response.headers.get("X-Bapi-Limit-Reset-Timestamp")
            if raw_reset is not None:
                try:
                    limit_reset_time = int(raw_reset)
                except (TypeError, ValueError):
                    # Malformed header — treat like a missing header rather
                    # than propagating an uncaught ValueError from the retry
                    # path.
                    self.logger.warning(
                        f"Malformed X-Bapi-Limit-Reset-Timestamp: {raw_reset!r}"
                    )
                    delay_time = self.retry_delay
                    limit_reset_str = "X-Bapi-Limit-Reset-Timestamp - malformed."
                else:
                    limit_reset_str = dt.fromtimestamp(
                        limit_reset_time / 10 ** 3
                    ).strftime("%H:%M:%S.%f")[:-3]
                    delay_time = (limit_reset_time - _helpers.generate_timestamp()) / 10 ** 3
            else:
                # Fall back to the user-configured retry_delay instead of a
                # hardcoded 5s so the CI test doesn't block for 5 real seconds
                # even when retry_delay=0, and so users can tune the fallback.
                delay_time = self.retry_delay
                limit_reset_str = "X-Bapi-Limit-Reset-Timestamp - not found in headers."
            error_msg = (
                f"API rate limit will reset at {limit_reset_str}. "
                f"Sleeping for {int(delay_time * 10 ** 3)} ms"
            )

        self.logger.error(f"{error_msg}. Retrying...")
        # Guard against pathological negative durations (clock skew, expired
        # reset timestamp) — asyncio.sleep accepts them but we log & clamp.
        await asyncio.sleep(max(0, delay_time))
        return recv_window

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
