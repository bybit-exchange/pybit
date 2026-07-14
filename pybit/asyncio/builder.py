from typing import Optional

from pybit import _http_manager


class RequestBuilder:
    """Reuse the sync signing/header helpers without spinning up an HTTP client."""

    def __init__(
            self,
            api_key: Optional[str],
            api_secret: Optional[str],
            rsa_authentication: bool,
            proxy: Optional[str] = None,
    ):
        self._http_manager = _http_manager._V5HTTPManager(
            api_key=api_key,
            api_secret=api_secret,
            rsa_authentication=rsa_authentication,
        )
        self._proxy = proxy

    def clean_query(self, query: Optional[dict]) -> dict:
        return self._http_manager._clean_query(query)

    def prepare_payload(self, method: str, parameters: dict) -> str:
        # Only short-circuit on GET — for POST an empty body must serialise
        # to "{}" so the signature bytes match the sync side (which calls
        # json.dumps({})). CDN/WAFs also expect a proper JSON body when
        # Content-Type is application/json.
        if method == "GET" and not parameters:
            return ""
        return self._http_manager.prepare_payload(method, parameters or {})

    def _auth(self, payload, recv_window, timestamp):
        return self._http_manager._auth(payload, recv_window, timestamp)

    def prepare_headers(self, payload: str, recv_window: int) -> dict:
        return self._http_manager._prepare_headers(payload, recv_window)

    def prepare_request(self, method: str, path: str, headers: dict, payload: str) -> dict:
        request = {
            "url": path,
            "headers": headers,
        }
        if method == "GET":
            if payload:
                request["url"] += f"?{payload}"
        else:
            request["data"] = payload
        if self._proxy:
            request["proxy"] = self._proxy
        return request
