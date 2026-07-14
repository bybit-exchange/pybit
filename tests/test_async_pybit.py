"""Async-side smoke tests: import parity, signature parity, retry behavior.

The retry tests mock aiohttp's ClientSession so nothing hits the network.
"""
import asyncio
import importlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from pybit._http_manager import _V5HTTPManager, _RetryableRequestError
from pybit.exceptions import FailedRequestError, InvalidRequestError


def _run(coro):
    """Test helper: run ``coro`` in a fresh event loop.

    Uses ``asyncio.run`` semantics (new loop per call) to avoid the
    ``get_event_loop()`` deprecation path on 3.12+.
    """
    return asyncio.run(coro)


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


def test_prepare_payload_post_empty_body_matches_sync():
    """CORR-01 regression: POST with empty params must serialise to "{}",
    matching sync's ``prepare_payload("POST", {})``. Anything else diverges
    the signature bytes for endpoints like request_demo_trading_funds."""
    from pybit.asyncio.builder import RequestBuilder

    builder = RequestBuilder(
        api_key=_API_KEY,
        api_secret=_API_SECRET,
        rsa_authentication=False,
    )
    assert builder.prepare_payload("POST", {}) == "{}"
    assert builder.prepare_payload("POST", None) == "{}"
    # GET short-circuit still preserved.
    assert builder.prepare_payload("GET", {}) == ""


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
        _run(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, start_time=0.0)
        )
    # 10006 does not touch recv_window — should pass through unchanged.
    assert exc_info.value.recv_window == 5000


def test_handle_response_10002_expands_recv_window():
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 10002, "retMsg": "recv_window"})

    with pytest.raises(_RetryableRequestError) as exc_info:
        _run(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, start_time=0.0)
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
        _run(
            c._handle_response(resp, "GET", "/x", "", recv_window=5000, start_time=0.0)
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

    result = _run(
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

    result = _run(
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
        _run(
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
        _run(
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
    _run(c.close_connection())


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
    mgr = c.futures_kline_stream(topics=["kline.60.BTCUSDT"])
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


def test_pong_recognized_via_ret_msg_field():
    """ASYNC-09: Bybit sends ``{"op":"ping","ret_msg":"pong",...}`` — the
    old code only checked ``op == "pong"`` and would leave _last_pong stale."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )
    m.ws_state = WSState.STREAMING
    m._last_pong = 0.0

    # Bybit's real pong shape:
    _run(m._process_frame({
        "op": "ping",
        "ret_msg": "pong",
        "success": True,
    }))
    assert m._last_pong > 0.0


def test_pong_recognized_via_op_field():
    """Belt-and-braces: the plain ``op == "pong"`` form still works."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )
    m.ws_state = WSState.STREAMING
    m._last_pong = 0.0

    _run(m._process_frame({"op": "pong"}))
    assert m._last_pong > 0.0


def test_demo_flag_flows_to_manager():
    """ASYNC-06: passing demo=True on the client must land on the manager
    so it can pick DEMO_SUBDOMAIN_* when connecting."""
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(channel_type="linear", testnet=True, demo=True)
    mgr = c.futures_kline_stream(topics=["kline.60.BTCUSDT"])
    assert mgr.demo is True


def test_public_wss_honors_tld():
    """ASYNC-07: the public URL must contain a {TLD} placeholder that the
    tld kwarg can replace."""
    from pybit.asyncio.ws.client import PUBLIC_WSS

    assert "{TLD}" in PUBLIC_WSS
    # And the {DOMAIN} placeholder is present too.
    assert "{DOMAIN}" in PUBLIC_WSS


def test_legacy_ret_code_error_not_silently_dropped():
    """CORR-09: ret_code (legacy P2P/OTC form) must be recognised, not
    treated as success."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(api_key=_API_KEY, api_secret=_API_SECRET, retry_delay=0)
    resp = _make_response_mock(200, {"ret_code": 10001, "ret_msg": "bad param"})
    _install_session(c, [resp])

    with pytest.raises(InvalidRequestError) as exc_info:
        _run(
            c._submit_request(
                method="POST",
                path="https://api-testnet.bybit.com/v5/p2p/item/info",
                query={"itemId": "1"},
                auth=True,
            )
        )
    assert "bad param" in str(exc_info.value)


def test_record_request_time_returns_timedelta():
    """CORR-03: parity with sync — response_time is a timedelta."""
    from datetime import timedelta
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(record_request_time=True, retry_delay=0)
    resp = _make_response_mock(200, {"retCode": 0, "retMsg": "OK", "result": {}})
    _install_session(c, [resp])

    result = _run(
        c._submit_request(
            method="GET",
            path="https://api-testnet.bybit.com/v5/market/time",
            query={},
        )
    )
    payload, elapsed = result
    assert payload["retCode"] == 0
    assert isinstance(elapsed, timedelta)


def test_submit_request_rejects_after_close():
    """ASYNC-04: post-close submission raises a clean FailedRequestError
    rather than AttributeError on ``getattr(None, method)``."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    _run(c.close_connection())
    assert c._closed is True

    with pytest.raises(FailedRequestError):
        _run(
            c._submit_request(
                method="GET",
                path="https://api-testnet.bybit.com/v5/market/time",
                query={},
            )
        )


def test_async_client_no_longer_accepts_loop_kwarg():
    """ASYNC-14: the deprecated ``loop`` kwarg has been removed."""
    from pybit.asyncio.client import AsyncClient

    with pytest.raises(TypeError):
        AsyncClient(loop="unused")


def test_async_account_no_mro_clash_with_market():
    """API-03 regression: account/instruments-info must be reachable."""
    from pybit.asyncio.unified_trading import AsyncHTTP

    assert hasattr(AsyncHTTP, "get_account_instruments_info")
    # Market's get_instruments_info still there:
    assert hasattr(AsyncHTTP, "get_instruments_info")


def test_set_no_convert_repay_enum_reachable():
    """API-02: Account.NO_CONVERT_REPAY must resolve at import time.

    Both ``manual_no_convert_repay`` (current) and ``set_no_convert_repay``
    (deprecated alias) are exposed to keep the previously-released API
    reachable for one release cycle.
    """
    from pybit.account import Account
    from pybit.asyncio.unified_trading import AsyncHTTP

    assert str(Account.NO_CONVERT_REPAY) == "/v5/account/no-convert-repay"
    assert hasattr(AsyncHTTP, "manual_no_convert_repay")
    assert hasattr(AsyncHTTP, "set_no_convert_repay")


def test_affiliate_sub_list_available():
    """API-01: AsyncUserHTTP.get_affiliate_sub_list is not missing."""
    from pybit.asyncio.unified_trading import AsyncHTTP

    assert hasattr(AsyncHTTP, "get_affiliate_sub_list")


def test_module_logger_uses_null_handler_only():
    """QUAL-04 / CORR-14: instantiating AsyncClient must not attach a
    StreamHandler to the module logger — that duplicates output when the
    host app configures logging."""
    import logging as _logging
    from pybit.asyncio.client import AsyncClient

    logger = _logging.getLogger("pybit.asyncio.client")
    for h in list(logger.handlers):
        # A NullHandler is fine; no StreamHandler should be present.
        assert not isinstance(h, _logging.StreamHandler) or isinstance(h, _logging.NullHandler)

    AsyncClient()
    for h in logger.handlers:
        assert not isinstance(h, _logging.StreamHandler) or isinstance(h, _logging.NullHandler)


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

    _run(m._auth())
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
        _run(m._auth())


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
        _run(m._auth())


# ---------------------------------------------------------------------------
# HTTP retry-branch coverage: network errors, JSON errors, non-200 status.
# ---------------------------------------------------------------------------

def _install_side_effects(client, side_effects):
    """Wire a session whose ``get``/``post`` raise/return per-call side effects.

    ``side_effects`` items are either exception classes/instances (raised on
    the corresponding call) or MagicMock responses (returned as the async
    context-manager result).
    """
    it = iter(side_effects)

    def _method_stub(**kwargs):
        v = next(it)
        if isinstance(v, BaseException) or (
            isinstance(v, type) and issubclass(v, BaseException)
        ):
            raise v
        return v

    session = MagicMock()
    session.get = MagicMock(side_effect=_method_stub)
    session.post = MagicMock(side_effect=_method_stub)
    session.close = AsyncMock()
    client._session = session
    return session


def test_force_retry_network_error_recovers():
    """L11a: with ``force_retry=True``, a transient ClientConnectionError
    triggers a retry and the next successful response is returned."""
    import aiohttp
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY, api_secret=_API_SECRET,
        retry_delay=0, force_retry=True, max_retries=3,
    )

    ok = _make_response_mock(200, {"retCode": 0, "retMsg": "OK", "result": {}})
    _install_side_effects(c, [aiohttp.ClientConnectionError("boom"), ok])

    result = _run(
        c._submit_request(
            method="GET",
            path="https://api-testnet.bybit.com/v5/market/tickers",
            query={"category": "linear"},
        )
    )
    assert result["retCode"] == 0


def test_network_error_without_force_retry_propagates():
    """L11a: without force_retry, a ClientConnectionError is surfaced to the
    caller (wrapped as FailedRequestError) instead of retried silently."""
    import aiohttp
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY, api_secret=_API_SECRET,
        retry_delay=0, force_retry=False, max_retries=3,
    )
    _install_side_effects(c, [aiohttp.ClientConnectionError("boom")])

    # _handle_network_error re-raises when force_retry is False. That escapes
    # the retry loop before the loop-exit FailedRequestError can fire, so
    # callers see the underlying aiohttp error.
    with pytest.raises(aiohttp.ClientConnectionError):
        _run(
            c._submit_request(
                method="GET",
                path="https://api-testnet.bybit.com/v5/market/tickers",
                query={"category": "linear"},
            )
        )


def test_force_retry_json_error_recovers():
    """L11b: JSON decode errors on a bad body → retry when force_retry.

    ``json.JSONDecodeError`` is the branch we care about here — aiohttp's
    ``ContentTypeError`` extends ``ClientResponseError`` and is dispatched
    through ``_handle_network_error``, so the JSON-specific handler is only
    exercised by real decode errors on a valid content-type response.
    """
    from json import JSONDecodeError
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY, api_secret=_API_SECRET,
        retry_delay=0, force_retry=True, max_retries=3,
    )

    bad = _make_response_mock(200, {})
    bad.json = AsyncMock(side_effect=JSONDecodeError("bad", "junk", 0))
    ok = _make_response_mock(200, {"retCode": 0, "retMsg": "OK"})
    _install_side_effects(c, [bad, ok])

    result = _run(
        c._submit_request(
            method="GET",
            path="https://api-testnet.bybit.com/v5/market/tickers",
            query={"category": "linear"},
        )
    )
    assert result["retCode"] == 0


def test_json_error_without_force_retry_reports_method_path():
    """L11b + L3: terminal FailedRequestError from _handle_json_error carries
    method / path / params context, not the generic ``"JSON decoding"``."""
    from json import JSONDecodeError
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(
        api_key=_API_KEY, api_secret=_API_SECRET,
        retry_delay=0, force_retry=False, max_retries=1,
    )

    bad = _make_response_mock(200, {})
    bad.json = AsyncMock(side_effect=JSONDecodeError("bad", "junk", 0))
    _install_side_effects(c, [bad])

    with pytest.raises(FailedRequestError) as exc_info:
        _run(
            c._submit_request(
                method="POST",
                path="/v5/order/create",
                query={"category": "linear"},
                auth=True,
            )
        )
    assert "POST" in str(exc_info.value)
    assert "/v5/order/create" in str(exc_info.value)


def test_check_status_code_403_message():
    """L12: 403 must produce the IP-rate-limit / US-IP message,
    not the generic non-200 one. FailedRequestError lowercases messages."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(403, {})

    with pytest.raises(FailedRequestError) as exc_info:
        _run(c._check_status_code(resp, "GET", "/x", ""))
    assert exc_info.value.status_code == 403
    assert "ip rate limit" in str(exc_info.value).lower()


def test_check_status_code_500_generic_message():
    """L12: 500 falls back to the generic non-200 message."""
    from pybit.asyncio.client import AsyncClient

    c = AsyncClient(retry_delay=0)
    resp = _make_response_mock(500, {})

    with pytest.raises(FailedRequestError) as exc_info:
        _run(c._check_status_code(resp, "GET", "/x", ""))
    assert exc_info.value.status_code == 500
    assert "not 200" in str(exc_info.value).lower()


def test_handle_retryable_error_clamps_upper_bound(monkeypatch):
    """L23: a far-future X-Bapi-Limit-Reset-Timestamp must not cause a
    minutes-long uninterruptible-except-cancel sleep."""
    from pybit.asyncio.client import AsyncClient

    # Pin ``now`` so we can compute a reset one hour in the future
    # deterministically.
    now_ms = 1_700_000_000_000
    monkeypatch.setattr(
        "pybit.asyncio.client._helpers.generate_timestamp", lambda: now_ms
    )

    c = AsyncClient(retry_delay=0)
    reset_ms = now_ms + 3_600_000  # +1 hour → raw delay 3600s
    resp = _make_response_mock(
        200,
        {"retCode": 10006, "retMsg": "rate limit"},
        headers={"X-Bapi-Limit-Reset-Timestamp": str(reset_ms)},
    )

    slept = []

    async def _fake_sleep(t):
        slept.append(t)

    monkeypatch.setattr("pybit.asyncio.client.asyncio.sleep", _fake_sleep)
    _run(
        c._handle_retryable_error(resp, 10006, "rate limit", recv_window=5000)
    )
    # Raw would be 3600; clamp caps at 30.
    assert slept == [30]


# ---------------------------------------------------------------------------
# WS state-machine regressions for the fixes in this PR.
# ---------------------------------------------------------------------------

def test_non_auth_subscribe_error_surfaces_without_reconnect():
    """H1 regression: subscribe ``success=false`` without ``"not authorized"``
    must enqueue the error frame and KEEP THE SOCKET ALIVE — not switch to
    RECONNECTING (which would spin a tear-down / rebuild storm because the
    same failing subscription is replayed on every reconnect).
    """
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=["sub-1"],
    )
    m.ws_state = WSState.STREAMING

    frame = {
        "op": "subscribe",
        "success": False,
        "ret_msg": "Invalid symbol: FOO",
    }
    _run(m._process_frame(frame))

    # State must be preserved.
    assert m.ws_state == WSState.STREAMING
    # Frame must reach the consumer.
    got = m.queue.get_nowait()
    assert got is frame


def test_unauthorized_subscribe_error_transitions_to_exiting():
    """Complement to the H1 regression: the ``"not authorized"`` branch
    still terminates the stream (unchanged behavior)."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    m = AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
    )
    m.ws_state = WSState.STREAMING

    _run(m._process_frame({
        "op": "subscribe",
        "success": False,
        "ret_msg": "Request not authorized",
    }))
    assert m.ws_state == WSState.EXITING
    got = m.queue.get_nowait()
    assert got["success"] is False


def test_auth_raises_auth_failed_error_subtype():
    """M5 regression: _auth raises the AuthFailedError subclass on server
    reject, so connect() can distinguish credential rejection from generic
    transport failures."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, AuthFailedError

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
        return _json.dumps({"op": "auth", "success": False, "ret_msg": "invalid signature"})

    ws_mock = MagicMock()
    ws_mock.send = _send
    ws_mock.recv = _recv
    m.ws = ws_mock

    with pytest.raises(AuthFailedError, match="invalid signature"):
        _run(m._auth())
    # AuthFailedError must remain a ConnectionError subclass for any caller
    # already catching that type.
    assert issubclass(AuthFailedError, ConnectionError)


def test_connect_bails_immediately_on_auth_failed():
    """M5 regression: AuthFailedError inside connect() short-circuits to
    EXITING with a single ``op=auth`` sentinel — no MAX_RECONNECTS storm."""
    from pybit.asyncio.ws import manager as manager_mod
    from pybit.asyncio.ws.manager import (
        AsyncWebsocketManager, AuthFailedError, WSState,
    )

    m = AsyncWebsocketManager(
        channel_type="private",
        url="wss://x/y",
        subscription_message=[],
        api_key=_API_KEY,
        api_secret=_API_SECRET,
    )

    open_calls = []

    async def _fake_open():
        open_calls.append(1)
        m.ws = MagicMock()

    async def _fake_close():
        m.ws = None

    async def _fake_auth():
        raise AuthFailedError("WS auth failed: bad key")

    m._open_conn = _fake_open
    m._close_conn = _fake_close
    m._auth = _fake_auth

    _run(m.connect())

    assert m.ws_state == WSState.EXITING
    # Exactly one attempt — no retry storm.
    assert len(open_calls) == 1
    # Consumer sees a single auth sentinel with the terminal contract.
    sentinel = m.queue.get_nowait()
    assert sentinel == {
        "type": "terminal",
        "reason": "auth_failed",
        "success": False,
        "ret_msg": "WS auth failed: bad key",
        "op": "auth",
    }
    assert m.queue.empty()


def test_keepalive_exits_on_state_exiting(monkeypatch):
    """M2 regression: _keepalive_task must break out when ws_state becomes
    EXITING instead of sleeping forever at PING_INTERVAL."""
    from pybit.asyncio.ws import manager as manager_mod
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    monkeypatch.setattr(manager_mod, "PING_INTERVAL", 0.01)

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )
    # Start in STREAMING; flip to EXITING shortly after keepalive begins.
    m.ws_state = WSState.STREAMING
    m.ws = MagicMock()
    m.ws.send = AsyncMock()

    async def _drive():
        task = asyncio.ensure_future(m._keepalive_task())
        await asyncio.sleep(0.02)
        m.ws_state = WSState.EXITING
        # Should return by itself within a couple of PING_INTERVALs, not hang.
        await asyncio.wait_for(task, timeout=0.5)
        return task

    task = _run(_drive())
    assert task.done()
    assert task.exception() is None


def test_connect_max_reconnects_cancels_keepalive(monkeypatch):
    """M2 regression: when connect() exhausts MAX_RECONNECTS, an already-
    running keepalive task must be cancelled — otherwise consumers who drop
    the manager after seeing the "Max reconnect reached" sentinel leak it."""
    from pybit.asyncio.ws import manager as manager_mod
    from pybit.asyncio.ws.manager import AsyncWebsocketManager, WSState

    # Force MAX_RECONNECTS to 1 so the test doesn't loop 60 times.
    monkeypatch.setattr(AsyncWebsocketManager, "MAX_RECONNECTS", 1)
    # Zero out the backoff so the test doesn't wait.
    monkeypatch.setattr(manager_mod, "get_reconnect_wait", lambda attempt: 0)

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )

    # A pre-existing keepalive task (as if a prior successful connect had
    # started one and the connection later died).
    async def _keep_alive_forever():
        await asyncio.sleep(3600)

    async def _drive():
        # Capture the task reference *before* connect() clears the attribute
        # so we can assert on its state afterwards.
        m._keepalive = asyncio.ensure_future(_keep_alive_forever())
        ka_ref = m._keepalive

        async def _boom():
            raise ConnectionError("simulated transport failure")

        m._open_conn = _boom
        m._close_conn = AsyncMock()

        await m.connect()
        # Give the event loop a tick so the cancellation propagates.
        try:
            await ka_ref
        except asyncio.CancelledError:
            pass
        return ka_ref

    ka = _run(_drive())

    assert m.ws_state == WSState.EXITING
    # The task attribute is cleared and the underlying task cancelled.
    assert m._keepalive is None
    assert ka.cancelled() or ka.done()


def test_missing_async_deps_raises_actionable_error(monkeypatch):
    """M7: if aiohttp or websockets isn't installed, importing
    ``pybit.asyncio`` must raise ImportError with the ``pip install
    pybit[async]`` hint — not a cryptic ModuleNotFoundError three imports
    deep."""
    import builtins
    import sys
    from pybit.asyncio import _check_async_deps

    real_import = builtins.__import__

    def _blocking_import(name, *args, **kwargs):
        if name == "aiohttp" or name.startswith("aiohttp."):
            raise ImportError(f"No module named '{name}'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _blocking_import)

    with pytest.raises(ImportError, match=r"pip install \"pybit\[async\]\""):
        _check_async_deps()


def _sub_args(mgr, frame_index=0):
    """Extract the ``args`` list from ``subscription_message[frame_index]``."""
    import json as _json
    return _json.loads(mgr.subscription_message[frame_index])["args"]


def test_public_typed_factories_emit_expected_topics():
    """M3: sync-parity typed public factories produce the exact topic
    strings Bybit expects. Symbol fan-out and multi-arg shapes covered."""
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(channel_type="linear", testnet=True)

    assert _sub_args(c.orderbook_stream(50, "BTCUSDT")) == ["orderbook.50.BTCUSDT"]
    assert _sub_args(c.rpi_orderbook_stream("BTCUSDT")) == ["orderbook.rpi.BTCUSDT"]
    assert _sub_args(c.trade_stream(["BTCUSDT", "ETHUSDT"])) == [
        "publicTrade.BTCUSDT", "publicTrade.ETHUSDT",
    ]
    assert _sub_args(c.ticker_stream("BTCUSDT")) == ["tickers.BTCUSDT"]
    assert _sub_args(c.kline_stream(60, "BTCUSDT")) == ["kline.60.BTCUSDT"]
    assert _sub_args(c.all_liquidation_stream("BTCUSDT")) == ["allLiquidation.BTCUSDT"]
    assert _sub_args(c.lt_kline_stream(60, "BTC3LUSDT")) == ["kline_lt.60.BTC3LUSDT"]
    assert _sub_args(c.lt_ticker_stream("BTC3LUSDT")) == ["tickers_lt.BTC3LUSDT"]
    assert _sub_args(c.lt_nav_stream("BTC3LUSDT")) == ["lt.BTC3LUSDT"]
    assert _sub_args(c.insurance_pool_stream("USDT")) == ["insurance.USDT"]
    assert _sub_args(c.price_limit_stream("BTCUSDT")) == ["priceLimit.BTCUSDT"]


def test_private_typed_factories_emit_expected_topics():
    """M3: sync-parity typed private factories produce Bybit's canonical
    topic strings (position, order, execution, wallet, greeks, spread.*)."""
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(
        channel_type="private", testnet=True,
        api_key=_API_KEY, api_secret=_API_SECRET,
    )
    assert _sub_args(c.position_stream()) == ["position"]
    assert _sub_args(c.order_stream()) == ["order"]
    assert _sub_args(c.execution_stream()) == ["execution"]
    assert _sub_args(c.wallet_stream()) == ["wallet"]
    assert _sub_args(c.greek_stream()) == ["greeks"]
    assert _sub_args(c.spread_order_stream()) == ["spread.order"]
    assert _sub_args(c.spread_execution_stream()) == ["spread.execution"]
    assert _sub_args(c.fast_execution_stream()) == ["execution.fast"]
    assert _sub_args(c.fast_execution_stream("linear")) == ["execution.fast.linear"]


def test_system_status_stream_requires_misc_status_channel():
    """M3: system_status_stream must reject non-``misc/status`` channels
    and produce the canonical ``system.status`` topic on the right one."""
    from pybit import exceptions
    from pybit.asyncio.ws import AsyncWebsocketClient

    linear = AsyncWebsocketClient(channel_type="linear", testnet=True)
    with pytest.raises(exceptions.InvalidChannelTypeError):
        linear.system_status_stream()

    status = AsyncWebsocketClient(channel_type="misc/status", testnet=True)
    assert _sub_args(status.system_status_stream()) == ["system.status"]


def test_public_factories_reject_private_channel():
    """M3: guard rail — public typed factories refuse a private channel."""
    from pybit import exceptions
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(
        channel_type="private", testnet=True,
        api_key=_API_KEY, api_secret=_API_SECRET,
    )
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.orderbook_stream(1, "BTCUSDT")
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.trade_stream("BTCUSDT")


def test_private_factories_reject_public_channel():
    """M3: guard rail — private typed factories refuse a public channel."""
    from pybit import exceptions
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(channel_type="linear", testnet=True)
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.position_stream()
    with pytest.raises(exceptions.InvalidChannelTypeError):
        c.wallet_stream()


def test_spot_typed_factory_chunks_subscribe_frames():
    """M3: spot channel splits subscribe frames at
    ``SPOT_MAX_CONNECTION_ARGS`` — 15 symbols → 10 + 5."""
    from pybit.asyncio.ws import AsyncWebsocketClient

    c = AsyncWebsocketClient(channel_type="spot", testnet=True)
    syms = [f"SYM{i}USDT" for i in range(15)]
    mgr = c.orderbook_stream(1, syms)
    assert len(mgr.subscription_message) == 2
    assert len(_sub_args(mgr, 0)) == 10
    assert len(_sub_args(mgr, 1)) == 5


def test_close_connection_emits_terminal_sentinel():
    """L7: user_close terminal sentinel carries ``type=terminal`` +
    ``reason=user_close`` so consumers can identify stream shutdown
    without inspecting per-path ``success`` flags."""
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )
    # No keepalive / read loop running, no ws — close_connection should
    # still terminate cleanly and enqueue the sentinel.
    _run(m.close_connection())
    sentinel = m.queue.get_nowait()
    assert sentinel["type"] == "terminal"
    assert sentinel["reason"] == "user_close"
    assert sentinel["success"] is True


def test_max_reconnect_emits_terminal_sentinel(monkeypatch):
    """L7: max-reconnect terminal sentinel carries the terminal contract."""
    from pybit.asyncio.ws import manager as manager_mod
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    monkeypatch.setattr(AsyncWebsocketManager, "MAX_RECONNECTS", 1)
    monkeypatch.setattr(manager_mod, "get_reconnect_wait", lambda attempt: 0)

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )

    async def _boom():
        raise ConnectionError("transport dead")

    m._open_conn = _boom
    m._close_conn = AsyncMock()

    _run(m.connect())
    sentinel = m.queue.get_nowait()
    assert sentinel["type"] == "terminal"
    assert sentinel["reason"] == "max_reconnect"
    assert sentinel["success"] is False


def test_connect_logs_empty_subscription(caplog):
    """L8 regression: empty subscription_message logs an INFO warning so a
    misconfigured caller notices they'll never receive stream frames."""
    import logging as _logging
    from pybit.asyncio.ws import manager as manager_mod
    from pybit.asyncio.ws.manager import AsyncWebsocketManager

    m = AsyncWebsocketManager(
        channel_type="linear",
        url="wss://x/y",
        subscription_message=[],
    )

    ws_mock = MagicMock()
    ws_mock.send = AsyncMock()

    async def _open():
        m.ws = ws_mock

    m._open_conn = _open
    m._close_conn = AsyncMock()

    # Stop the read loop from actually running.
    m._read_loop = AsyncMock()
    m._keepalive_task = AsyncMock()

    with caplog.at_level(_logging.INFO, logger="pybit.asyncio.ws.manager"):
        _run(m.connect())

    combined = " ".join(r.getMessage() for r in caplog.records)
    assert "No subscription messages provided" in combined
