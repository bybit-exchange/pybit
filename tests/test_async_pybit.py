"""Async-side smoke tests: import parity, signature parity, retry behavior.

The retry tests mock aiohttp's ClientSession so nothing hits the network.
"""
import asyncio
import importlib
from json import JSONDecodeError
from unittest.mock import AsyncMock, MagicMock

import pytest

from pybit._http_manager import _V5HTTPManager, _RetryableRequestError
from pybit.exceptions import FailedRequestError, InvalidRequestError


_API_KEY = "CFEJUGQEQPPHGOHGHM"
_API_SECRET = "VDFZSSPUTKRJMXAVMJXBHEXIPZNZJIZUBVRQ"


# ---------------------------------------------------------------------------
# Import smoke: every renamed async module loads.
# ---------------------------------------------------------------------------

ASYNC_MODULES = [
    "pybit.asyncio",
    "pybit.asyncio.client",
    "pybit.asyncio.builder",
    "pybit.asyncio.unified_trading",
    "pybit.asyncio.utils",
    "pybit.asyncio.http",
    "pybit.asyncio.http._v5_account",
    "pybit.asyncio.http._v5_asset",
    "pybit.asyncio.http._v5_broker",
    "pybit.asyncio.http._v5_crypto_loan",
    "pybit.asyncio.http._v5_earn",
    "pybit.asyncio.http._v5_fiat",
    "pybit.asyncio.http._v5_institutional_loan",
    "pybit.asyncio.http._v5_market",
    "pybit.asyncio.http._v5_misc",
    "pybit.asyncio.http._v5_p2p",
    "pybit.asyncio.http._v5_position",
    "pybit.asyncio.http._v5_pre_upgrade",
    "pybit.asyncio.http._v5_rate_limit",
    "pybit.asyncio.http._v5_rfq",
    "pybit.asyncio.http._v5_spot_leverage_token",
    "pybit.asyncio.http._v5_spot_margin_trade",
    "pybit.asyncio.http._v5_spread",
    "pybit.asyncio.http._v5_trade",
    "pybit.asyncio.http._v5_user",
    "pybit.asyncio.ws",
    "pybit.asyncio.ws.client",
    "pybit.asyncio.ws.manager",
    "pybit.asyncio.ws.utils",
]


@pytest.mark.parametrize("module_name", ASYNC_MODULES)
def test_async_module_imports(module_name):
    importlib.import_module(module_name)


def test_async_http_class_composition():
    from pybit.asyncio.unified_trading import AsyncHTTP

    names = {c.__name__ for c in AsyncHTTP.__mro__}
    # Both former P2PHTTP / SpreadHTTP must now be prefixed.
    assert "AsyncP2PHTTP" in names
    assert "AsyncSpreadHTTP" in names
    assert "P2PHTTP" not in names
    assert "SpreadHTTP" not in names


# ---------------------------------------------------------------------------
# Signature parity: async RequestBuilder produces the same bytes as sync.
# ---------------------------------------------------------------------------

def test_signature_parity_sync_vs_async(monkeypatch):
    from pybit.asyncio.builder import RequestBuilder

    fixed_ts = 1_700_000_000_000
    monkeypatch.setattr(
        "pybit._http_manager._helpers.generate_timestamp",
        lambda: fixed_ts,
    )

    sync_manager = _V5HTTPManager(api_key=_API_KEY, api_secret=_API_SECRET)
    async_builder = RequestBuilder(
        api_key=_API_KEY,
        api_secret=_API_SECRET,
        rsa_authentication=False,
    )

    payload = "category=linear&symbol=BTCUSDT"
    recv_window = 5000

    sync_headers = sync_manager._prepare_headers(payload, recv_window)
    async_headers = async_builder.prepare_headers(payload, recv_window)

    assert sync_headers["X-BAPI-SIGN"] == async_headers["X-BAPI-SIGN"]
    assert sync_headers["X-BAPI-TIMESTAMP"] == async_headers["X-BAPI-TIMESTAMP"]
    assert sync_headers["X-BAPI-API-KEY"] == async_headers["X-BAPI-API-KEY"]
    assert sync_headers["X-BAPI-RECV-WINDOW"] == async_headers["X-BAPI-RECV-WINDOW"]


# ---------------------------------------------------------------------------
# AsyncClient default retry_codes / ignore_codes semantics.
# ---------------------------------------------------------------------------

def test_async_client_default_retry_and_ignore_codes():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient()
    # AC-02: retry codes default to the same set the sync client uses.
    assert c.retry_codes == {10002, 10006, 30034, 30035, 130035, 130150}
    assert c.ignore_codes == set()


def test_async_client_respects_explicit_empty_sets():
    """`is not None` guard: user-supplied empty sets are respected."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_codes=set(), ignore_codes=set())
    assert c.retry_codes == set()
    assert c.ignore_codes == set()


# ---------------------------------------------------------------------------
# Retry behavior: _handle_response signals via _RetryableRequestError, and
# _submit_request must catch it, rebind recv_window, and loop.
# ---------------------------------------------------------------------------

def _make_response_mock(status: int, json_payload: dict, headers: dict = None):
    """Build a mock aiohttp response that supports `async with` + `await .json()`."""
    resp = MagicMock()
    resp.status = status
    resp.headers = headers or {}
    resp.url = "https://api-testnet.bybit.com/v5/order/realtime"
    resp.json = AsyncMock(return_value=json_payload)
    resp.text = AsyncMock(return_value="")
    resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=False)
    return resp


def _install_session(client, responses):
    """Wire an in-memory session that returns each response in order."""
    it = iter(responses)

    def _method_stub(**kwargs):
        return next(it)

    session = MagicMock()
    session.get = MagicMock(side_effect=_method_stub)
    session.post = MagicMock(side_effect=_method_stub)
    session.close = AsyncMock()
    client._session = session
    return session


def test_handle_response_raises_retryable_sentinel():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 10006, "retMsg": "rate limited"})

    with pytest.raises(_RetryableRequestError) as exc_info:
        asyncio.get_event_loop().run_until_complete(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, response_time=0.0)
        )
    # 10006 does not touch recv_window — should pass through unchanged.
    assert exc_info.value.recv_window == 5000


def test_handle_response_10002_expands_recv_window():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 10002, "retMsg": "recv_window"})

    with pytest.raises(_RetryableRequestError) as exc_info:
        asyncio.get_event_loop().run_until_complete(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, response_time=0.0)
        )
    assert exc_info.value.recv_window == 7500


def test_handle_response_10006_missing_reset_header_does_not_raise():
    """AC-04: int(response.headers.get(...)) with a missing header must not TypeError."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 10006, "retMsg": "rate limited"})
    # No X-Bapi-Limit-Reset-Timestamp header at all.

    # Should raise the sentinel, not TypeError.
    with pytest.raises(_RetryableRequestError):
        asyncio.get_event_loop().run_until_complete(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, response_time=0.0)
        )


def test_submit_request_retries_and_expands_recv_window():
    """End-to-end: 10002 → loop → success with recv_window bumped to 7500."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(api_key=_API_KEY, api_secret=_API_SECRET, retry_delay=0)

    first = _make_response_mock(200, {"retCode": 10002, "retMsg": "recv_window"})
    second = _make_response_mock(200, {"retCode": 0, "retMsg": "OK", "result": {}})
    _install_session(c, [first, second])

    captured_recv_windows = []
    original_prepare = c._request_builder.prepare_headers

    def _spy_prepare(payload, recv_window):
        captured_recv_windows.append(recv_window)
        return original_prepare(payload, recv_window)

    c._request_builder.prepare_headers = _spy_prepare

    result = asyncio.get_event_loop().run_until_complete(
        c._submit_request(
            method="GET",
            path="https://api-testnet.bybit.com/v5/order/realtime",
            query={"category": "linear"},
            auth=True,
        )
    )

    assert result["retCode"] == 0
    assert captured_recv_windows == [5000, 7500]


def test_submit_request_ignores_ignored_codes():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY,
        api_secret=_API_SECRET,
        ignore_codes={110043},
        retry_delay=0,
    )
    resp = _make_response_mock(200, {"retCode": 110043, "retMsg": "leverage not changed"})
    _install_session(c, [resp])

    result = asyncio.get_event_loop().run_until_complete(
        c._submit_request(
            method="POST",
            path="https://api-testnet.bybit.com/v5/position/set-leverage",
            query={"category": "linear", "symbol": "BTCUSDT"},
            auth=True,
        )
    )
    assert result["retCode"] == 110043


def test_submit_request_raises_on_non_ignored_error():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(api_key=_API_KEY, api_secret=_API_SECRET, retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 10001, "retMsg": "parameter error"})
    _install_session(c, [resp])

    with pytest.raises(InvalidRequestError):
        asyncio.get_event_loop().run_until_complete(
            c._submit_request(
                method="POST",
                path="https://api-testnet.bybit.com/v5/order/create",
                query={},
                auth=True,
            )
        )


def test_submit_request_max_retries_exhausted():
    """AC-01 regression: repeated retry codes must eventually raise FailedRequestError."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY,
        api_secret=_API_SECRET,
        retry_delay=0,
        max_retries=3,
    )
    # Every response is a retryable error.
    responses = [
        _make_response_mock(200, {"retCode": 10006, "retMsg": "rate limited"})
        for _ in range(3)
    ]
    _install_session(c, responses)

    with pytest.raises(FailedRequestError):
        asyncio.get_event_loop().run_until_complete(
            c._submit_request(
                method="GET",
                path="https://api-testnet.bybit.com/v5/order/realtime",
                query={"category": "linear"},
                auth=True,
            )
        )


def test_close_connection_is_null_safe():
    """AC-11: close_connection tolerates being called without init_client()."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient()
    # No init_client() → _session is None. Must not raise.
    asyncio.get_event_loop().run_until_complete(c.close_connection())


def test_log_request_masks_api_key(caplog):
    import logging
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(log_requests=True, logging_level=logging.DEBUG)
    c.logger.setLevel(logging.DEBUG)
    for h in c.logger.handlers:
        h.setLevel(logging.DEBUG)

    with caplog.at_level(logging.DEBUG, logger="pybit.asyncio.client"):
        c._log_request(
            "GET",
            "/v5/order/realtime",
            "category=linear",
            {"X-BAPI-API-KEY": "secret-key-do-not-leak", "X-BAPI-SIGN": "abc"},
        )

    combined = " ".join(r.getMessage() for r in caplog.records)
    assert "secret-key-do-not-leak" not in combined
    assert "REDACTED" in combined


# ---------------------------------------------------------------------------
# AsyncWebsocketClient guard rails.
# ---------------------------------------------------------------------------

def test_user_streams_require_private_channel():
    from pybit import exceptions
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(channel_type="linear", testnet=True)
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.user_futures_stream()
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.user_spot_stream()


def test_private_channel_requires_keys():
    from pybit import exceptions
    from pybit.asyncio.ws import AsyncWebsocketClient

    with pytest.raises(exceptions.UnauthorizedExceptionError):
        AsyncWebsocketClient(channel_type="private", testnet=True)


def test_client_forwards_rsa_flag_and_proxy():
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(
        channel_type="private",
        testnet=True,
        api_key=_API_KEY,
        api_secret=_API_SECRET,
        rsa_authentication=True,
        proxy="http://user:pass@proxy.example:8080",
    )
    mgr = c.user_futures_stream()
    assert mgr.rsa_authentication is True
    assert mgr.proxy == "http://user:pass@proxy.example:8080"
    assert mgr.api_key == _API_KEY
    assert mgr.api_secret == _API_SECRET


def test_public_stream_does_not_leak_keys_but_forwards_proxy():
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(
        channel_type="linear",
        testnet=True,
        api_key="should-be-dropped",
        api_secret="should-be-dropped",
        proxy="http://proxy.example:8080",
    )
    mgr = c.futures_kline_stream(symbols=["kline.60.BTCUSDT"])
    assert mgr.api_key is None
    assert mgr.api_secret is None
    assert mgr.proxy == "http://proxy.example:8080"


def test_ws_manager_redacts_proxy_credentials():
    from pybit.asyncio.ws.manager import _redact_proxy

    assert _redact_proxy("http://user:pass@proxy.example:8080") == "proxy.example"
    assert _redact_proxy(None) == "<none>"
    assert _redact_proxy("") == "<none>"


def test_ws_manager_private_auth_expire_is_per_instance():
    """AC-12: PRIVATE_AUTH_EXPIRE is configurable per-instance, not module-level."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    m = AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
        private_auth_expire=7,
    )
    assert m.private_auth_expire == 7


def test_ws_auth_reads_ack_inline_and_succeeds():
    """Regression: _auth must read the ACK synchronously; delegating to the
    read loop deadlocks because the loop isn't reading during connect()."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    m = AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
        api_key=_API_KEY,
        api_secret=_API_SECRET,
    )

    sent = []

    async def _send(payload):
        sent.append(payload)

    async def _recv():
        # Bybit responds with success=True on good auth.
        import json as _json
        return _json.dumps({"op": "auth", "success": True, "ret_msg": ""})

    ws_mock = MagicMock()
    ws_mock.send = _send
    ws_mock.recv = _recv
    m.ws = ws_mock

    asyncio.get_event_loop().run_until_complete(m._auth())
    # sent one auth frame, no exception raised.
    assert len(sent) == 1
    import json as _json
    frame = _json.loads(sent[0])
    assert frame["op"] == "auth"
    assert frame["args"][0] == _API_KEY


def test_ws_auth_raises_on_server_reject():
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    m = AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
        api_key=_API_KEY,
        api_secret=_API_SECRET,
    )

    async def _send(_):
        pass

    async def _recv():
        import json as _json
        return _json.dumps({"op": "auth", "success": False, "ret_msg": "bad key"})

    ws_mock = MagicMock()
    ws_mock.send = _send
    ws_mock.recv = _recv
    m.ws = ws_mock

    with pytest.raises(ConnectionError, match="bad key"):
        asyncio.get_event_loop().run_until_complete(m._auth())


def test_ws_auth_raises_on_timeout(monkeypatch):
    """Auth ACK never arrives → ConnectionError, not hang."""
    from pybit.asyncio.ws import manager as manager_mod

    monkeypatch.setattr(manager_mod, "AUTH_ACK_TIMEOUT", 0.05)

    m = manager_mod.AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
        api_key=_API_KEY,
        api_secret=_API_SECRET,
    )

    async def _send(_):
        pass

    async def _recv():
        # Never returns — simulates a server that swallows the auth.
        await asyncio.sleep(10)

    ws_mock = MagicMock()
    ws_mock.send = _send
    ws_mock.recv = _recv
    m.ws = ws_mock

    with pytest.raises(ConnectionError, match="timed out"):
        asyncio.get_event_loop().run_until_complete(m._auth())
