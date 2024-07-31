import asyncio
from dataclasses import dataclass
from datetime import datetime as dt
from typing import (
    Optional,
    Union
)

import httpx
from pybit._http_manager._http_manager import (
    _V5HTTPManager,
    RET_MSG,
    RET_CODE
)
from pybit._http_manager._response_handler import ForceRetryException
from pybit._http_manager import _http_helpers
from pybit.exceptions import FailedRequestError, InvalidRequestError


@dataclass
class _AsyncV5HTTPManager(_V5HTTPManager):
    @staticmethod
    def _init_request_client() -> httpx.AsyncClient:
        return httpx.AsyncClient()

    async def close(self):
        await self.client.aclose()

    def _prepare_request(self,
                         recv_window: int,
                         method: str = None,
                         path: str = None,
                         query: dict = None,
                         auth: bool = False):
        req_params: Union[dict, str] = self.prepare_payload(method, query)

        # Authenticate if we are using a private endpoint.
        headers: dict = self._prepare_auth_headers(recv_window, req_params) if auth else {}

        if method == "GET":
            path = path + f"?{req_params}" if req_params else path
            data = None
        else:
            data = req_params

        return self.client.build_request(method, path, data=data, headers=headers)

    async def _submit_request(self,
                              method: Optional[str] = None,
                              path: Optional[str] = None,
                              query: Optional[dict] = None,
                              auth: bool = False):
        """
        Submits the request to the API.

        Notes
        -------------------
        We use the params argument for the GET method, and data argument for
        the POST method. Dicts passed to the data argument must be
        JSONified prior to submitting request.
        """

        query = {} if query is None else query

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

            req: httpx.Request = self._prepare_request(recv_window, method, path, query, auth)

            # Log the request.
            self._log_request(req_params, method, path, req.headers)

            try:
                # TODO make timeout
                response = await self.client.send(req, )
            except (
                httpx._exceptions.ReadTimeout,
                # TODO fill with network exceptions
            ) as e:
                if self.force_retry:
                    self.logger.error(f"{e}. {retries_remaining}")
                    await asyncio.sleep(self.retry_delay)
                    continue
                else:
                    raise e

            # Convert response to dictionary, or raise if requests error.
            try:
                res_json = self._convert_to_dict(response, method, path, req_params)
            except ForceRetryException as e:
                self.logger.error(f"{e}. {retries_remaining}")
                await asyncio.sleep(self.retry_delay)
                continue

            # If Bybit returns an error, raise.
            if res_json[RET_CODE]:
                # Generate error message.
                error_msg = f"{res_json[RET_MSG]} (ErrCode: {res_json[RET_CODE]})"

                # Set default retry delay.
                delay_time = self.retry_delay

                # Retry non-fatal whitelisted error requests.
                if res_json[RET_CODE] in self.retry_codes:
                    # 10002, recv_window error; add 2.5 seconds and retry.
                    if res_json[RET_CODE] == 10002:
                        error_msg += ". Added 2.5 seconds to recv_window"
                        recv_window += 2500

                    # 10006, rate limit error; wait until
                    # X-Bapi-Limit-Reset-Timestamp and retry.
                    elif res_json[RET_CODE] == 10006:
                        self.logger.error(
                            f"{error_msg}. Hit the API rate limit. "
                            f"Sleeping, then trying again. Request: {path}"
                        )

                        delay_time, limit_reset_str = _http_helpers.calculate_rate_limit_delay_time(int(response.headers["X-Bapi-Limit-Reset-Timestamp"]))
                        error_msg = (
                            f"API rate limit will reset at {limit_reset_str}. "
                            f"Sleeping for {int(delay_time * 10**3)} milliseconds"
                        )

                    # Log the error.
                    self.logger.error(f"{error_msg}. {retries_remaining}")
                    await asyncio.sleep(delay_time)
                    continue

                elif res_json[RET_CODE] in self.ignore_codes:
                    pass

                else:
                    raise InvalidRequestError(
                        request=f"{method} {path}: {req_params}",
                        message=res_json[RET_MSG],
                        status_code=res_json[RET_CODE],
                        time=dt.utcnow().strftime("%H:%M:%S"),
                        resp_headers=response.headers,
                    )
            else:
                if self.log_requests:
                    self.logger.debug(
                        f"Response headers: {response.headers}"
                    )

                if self.return_response_headers:
                    # TODO elapsed
                    return res_json, response.elapsed, response.headers,
                elif self.record_request_time:
                    return res_json, response.elapsed
                else:
                    return res_json
