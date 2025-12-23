from typing import Optional

from pybit import _http_manager


class RequestBuilder:
    def __init__(
            self,
            api_key: str,
            api_secret: str,
            rsa_authentication: bool,
            proxy: Optional[str] = None
    ):
        self._http_manager = _http_manager._V5HTTPManager(
            api_key=api_key,
            api_secret=api_secret,
            rsa_authentication=rsa_authentication
        )
        self._proxy = proxy

    def clean_query(self, query: Optional[dict]) -> dict:
        return self._http_manager._clean_query(query)

    def prepare_payload(self, method: str, parameters: dict) -> Optional[str]:
        if not parameters:
            return None
        return self._http_manager.prepare_payload(method, parameters)

    def _auth(self, payload, recv_window, timestamp):
        return self._http_manager._auth(payload, recv_window, timestamp)

    def prepare_headers(self, payload: str, recv_window: int) -> dict:
        return self._http_manager._prepare_headers(payload, recv_window)

    def prepare_request(self, method:str, path: str, headers: dict, payload: str) -> dict:
        request = {
            "url": path,
            "headers": headers,
        }
        if method == "GET":
            request["url"] += f"?{payload}"
        else:
            request["data"] = payload
        if self._proxy:
            request["proxy"] = self._proxy
        return request
