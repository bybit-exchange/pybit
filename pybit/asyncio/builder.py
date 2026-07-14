from typing import Optional

from pybit import _http_manager


def _build_signing_manager(
        api_key: Optional[str],
        api_secret: Optional[str],
        rsa_authentication: bool,
) -> "_http_manager._V5HTTPManager":
    """Construct a ``_V5HTTPManager`` for signing only, bypassing the
    dataclass ``__post_init__``.

    A plain ``_V5HTTPManager(api_key=..., api_secret=...)`` triggers
    ``__post_init__``, which (a) opens a ``requests.Session()`` — held for
    the lifetime of the async client and never used — and (b) attaches a
    ``logging.StreamHandler`` to the pybit logger when the root logger has
    no handlers. Both undo ``AsyncClient``'s own docstring promise of
    'the application decides where logs go' and pull ``requests`` into the
    async runtime dep set for no reason. This helper materialises just the
    fields the signing / header / payload helpers actually read.
    """
    inst = _http_manager._V5HTTPManager.__new__(_http_manager._V5HTTPManager)
    inst.api_key = api_key
    inst.api_secret = api_secret
    inst.rsa_authentication = rsa_authentication
    # ``_prepare_headers`` reads ``recv_window`` only via the caller-passed
    # arg, but ``_clean_query`` / ``prepare_payload`` don't need any other
    # dataclass fields. Set the ones referenced defensively so a future
    # helper reading e.g. ``self.retry_codes`` doesn't ``AttributeError``.
    return inst


class RequestBuilder:
    """Reuse the sync signing/header helpers without spinning up an HTTP client."""

    def __init__(
            self,
            api_key: Optional[str],
            api_secret: Optional[str],
            rsa_authentication: bool,
            proxy: Optional[str] = None,
    ):
        self._http_manager = _build_signing_manager(
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
