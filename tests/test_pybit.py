import logging
import io

import pytest
import hmac
import hashlib
from collections import defaultdict
from unittest.mock import Mock

import requests
import websocket

from pybit._http_manager import _V5HTTPManager
from pybit._websocket_stream import _WebSocketManager
from pybit.unified_trading import HTTP
from pybit import _http_manager

_api_key = "CFEJUGQEQPPHGOHGHM"
_api_secret = "VDFZSSPUTKRJMXAVMJXBHEXIPZNZJIZUBVRQ"


@pytest.fixture
def hmac_secret():
    return _api_secret


@pytest.fixture
def sample_param_str():
    return "12345mykey6789payload"


@pytest.fixture
def http():
    # Create a manager instance for testing
    return HTTP(testnet=True, api_key=_api_key, api_secret=_api_secret)


def test_generate_signature_hmac(hmac_secret, sample_param_str):
    # HMAC signature should match direct hmac calculation
    expected = hmac.new(
        bytes(hmac_secret, 'utf-8'),
        sample_param_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    assert _http_manager.generate_signature(False, hmac_secret, sample_param_str) == expected


@pytest.mark.parametrize("method,params,expected", [
    ("GET", {"a": 1, "b": None, "c": 3}, "a=1&c=3"),
    ("POST", {"qty": 10, "price": 100.0, "other": "x"}, None),
])
def test_prepare_payload(method, params, expected):
    payload = _V5HTTPManager.prepare_payload(method, params.copy())
    if method == "GET":
        assert payload == expected
    else:
        # price & qty should be cast to string
        assert '"qty": "10"' in payload
        assert '"price": "100.0"' in payload
        assert '"other": "x"' in payload


@pytest.mark.parametrize("query,expected", [
    (None, {}),
    ({'a': 1.0, 'b': 2.5, 'c': None}, {'a':1, 'b':2.5}),
])
def test_clean_query(http, query, expected):
    result = http._clean_query(query)
    assert result == expected


def test_get_server_time_direct(http):
    """
    Ensure HTTP availability of Bybit API using pybit
    """
    resp = http.get_server_time()["result"]
    assert isinstance(resp, dict)
    assert 'timeSecond' in resp and 'timeNano' in resp
    assert resp['timeSecond'].isdigit()
    assert resp['timeNano'].isdigit()


# --- ensuring correct init ---
@pytest.mark.parametrize("testnet, demo, domain, expected_endpoint", [
    # mainnet (testnet=False, demo=False)
    (False, False, None, "https://api.bybit.com"),
    # mainnet + custom domain
    (False, False, "bytick", "https://api.bytick.com"),
    # testnet only
    (True, False, None, "https://api-testnet.bybit.com"),
    # testnet + demo
    (True, True, None, "https://api-demo-testnet.bybit.com"),
    # demo only
    (False, True, None, "https://api-demo.bybit.com"),
])
def test_endpoint_variations(testnet, demo, domain, expected_endpoint):
    kwargs = {"testnet": testnet, "demo": demo}
    if domain is not None:
        kwargs["domain"] = domain
    m = _V5HTTPManager(**kwargs)
    assert m.endpoint == expected_endpoint


def test_default_retry_and_ignore_codes():
    m = _V5HTTPManager()
    # empty ignore_codes stays empty
    assert m.ignore_codes == set()
    # retry_codes should be set to the default set
    assert isinstance(m.retry_codes, set)


def test_http_session_headers_and_timeout():
    m = _V5HTTPManager()
    # client should be a requests.Session
    assert isinstance(m.client, requests.Session)
    # default headers
    hdrs = m.client.headers
    assert hdrs["Content-Type"] == "application/json"
    assert hdrs["Accept"] == "application/json"
    # default timeout
    assert m.timeout == 10


def test_referral_id_sets_header():
    ref = "pybit"
    m = _V5HTTPManager(referral_id=ref)
    assert m.client.headers["Referer"] == ref

def test_logger_handler_attached():
    # create with a fresh logging root
    # temporarily remove all handlers from root
    root = logging.root
    old_handlers = list(root.handlers)
    for h in old_handlers:
        root.removeHandler(h)

    try:
        m = _V5HTTPManager(logging_level=logging.DEBUG)
        # Our logger should have at least one handler
        handlers = m.logger.handlers
        assert len(handlers) >= 1
        # And that handler should be set to the manager's logging level
        assert handlers[0].level == logging.DEBUG
    finally:
        # restore original handlers
        root.handlers = old_handlers


class _FakeSock:
    def __init__(self, connected=True):
        self.connected = connected


class _FakeWS:
    def __init__(self, connected=True, send_error=None):
        self.sock = _FakeSock(connected=connected)
        self.send_error = send_error
        self.sent_messages = []
        self.closed = False

    def send(self, message):
        if self.send_error is not None:
            raise self.send_error
        self.sent_messages.append(message)

    def close(self):
        self.closed = True
        self.sock = None


class _FakeTimer:
    def __init__(self):
        self.daemon = False
        self.started = False
        self.cancelled = False

    def start(self):
        self.started = True

    def cancel(self):
        self.cancelled = True


def test_websocket_exit_cancels_custom_ping_timer():
    manager = _WebSocketManager(
        lambda _: None,
        "Test WS",
        testnet=False,
    )
    manager.ws = _FakeWS()
    timer = _FakeTimer()
    manager.custom_ping_timer = timer

    manager.exit()

    assert manager.exited is True
    assert timer.cancelled is True
    assert manager.custom_ping_timer is None
    assert manager.ws.closed is True


def test_send_custom_ping_ignores_closed_connection():
    manager = _WebSocketManager(
        lambda _: None,
        "Test WS",
        testnet=False,
    )
    manager.ws = _FakeWS(
        connected=True,
        send_error=websocket.WebSocketConnectionClosedException(
            "Connection is already closed."
        ),
    )

    manager._send_custom_ping()


def test_send_custom_ping_skips_disconnected_socket():
    manager = _WebSocketManager(
        lambda _: None,
        "Test WS",
        testnet=False,
    )
    manager.ws = _FakeWS(connected=False)

    manager._send_custom_ping()

    assert manager.ws.sent_messages == []


def test_websocket_exit_waits_with_sleep_until_socket_closes(monkeypatch):
    manager = _WebSocketManager(
        lambda _: None,
        "Test WS",
        testnet=False,
    )

    class _SlowCloseWS:
        def __init__(self):
            self._sock = object()
            self.close_called = False

        @property
        def sock(self):
            return self._sock

        @sock.setter
        def sock(self, value):
            self._sock = value

        def close(self):
            self.close_called = True

    manager.ws = _SlowCloseWS()
    sleep_calls = []

    def fake_sleep(delay):
        sleep_calls.append(delay)
        manager.ws.sock = None

    monkeypatch.setattr("pybit._websocket_stream.time.sleep", fake_sleep)

    manager.exit()

    assert manager.ws.close_called is True
    assert sleep_calls == [0.01]


def test_submit_request_retries_when_retcode_is_retryable():
    manager = _V5HTTPManager(api_key=_api_key, api_secret=_api_secret)
    manager.retry_delay = 0

    first_response = Mock()
    first_response.status_code = 200
    first_response.headers = {}
    first_response.elapsed = 0
    first_response.url = "https://api.bybit.com/v5/order/realtime"
    first_response.json.return_value = {
        "retCode": 10006,
        "retMsg": "Too many visits",
        "result": {},
        "time": 1234567890,
    }

    second_response = Mock()
    second_response.status_code = 200
    second_response.headers = {}
    second_response.elapsed = 0
    second_response.url = "https://api.bybit.com/v5/order/realtime"
    second_response.json.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": []},
        "time": 1234567891,
    }

    manager.client.send = Mock(side_effect=[first_response, second_response])

    result = manager._submit_request(
        method="GET",
        path="https://api.bybit.com/v5/order/realtime",
        query={"category": "linear"},
        auth=True,
    )

    assert result["retCode"] == 0
    assert manager.client.send.call_count == 2


def test_submit_request_retries_with_expanded_recv_window_after_10002():
    manager = _V5HTTPManager(api_key=_api_key, api_secret=_api_secret)
    manager.retry_delay = 0

    first_response = Mock()
    first_response.status_code = 200
    first_response.headers = {}
    first_response.elapsed = 0
    first_response.url = "https://api.bybit.com/v5/order/realtime"
    first_response.json.return_value = {
        "retCode": 10002,
        "retMsg": "invalid request, please check your server timestamp or recv_window param",
        "result": {},
        "time": 1234567890,
    }

    second_response = Mock()
    second_response.status_code = 200
    second_response.headers = {}
    second_response.elapsed = 0
    second_response.url = "https://api.bybit.com/v5/order/realtime"
    second_response.json.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"list": []},
        "time": 1234567891,
    }

    captured_recv_windows = []

    def fake_prepare_headers(payload, recv_window):
        captured_recv_windows.append(recv_window)
        return {}

    manager._prepare_headers = fake_prepare_headers
    manager.client.send = Mock(side_effect=[first_response, second_response])

    result = manager._submit_request(
        method="GET",
        path="https://api.bybit.com/v5/order/realtime",
        query={"category": "linear"},
        auth=True,
    )

    assert result["retCode"] == 0
    assert manager.client.send.call_count == 2
    assert captured_recv_windows == [5000, 7500]


def test_submit_request_returns_response_when_retcode_is_ignored():
    manager = _V5HTTPManager(api_key=_api_key, api_secret=_api_secret)
    manager.ignore_codes.add(110043)

    ignored_response = Mock()
    ignored_response.status_code = 200
    ignored_response.headers = {}
    ignored_response.elapsed = 0
    ignored_response.url = "https://api-testnet.bybit.com/v5/position/set-leverage"
    ignored_response.json.return_value = {
        "retCode": 110043,
        "retMsg": "leverage not changed",
        "result": {},
        "retExtInfo": {},
        "time": 1234567890,
    }

    manager.client.send = Mock(return_value=ignored_response)

    result = manager._submit_request(
        method="POST",
        path="https://api-testnet.bybit.com/v5/position/set-leverage",
        query={
            "category": "linear",
            "symbol": "BTCUSDT",
            "buyLeverage": "10",
            "sellLeverage": "10",
        },
        auth=True,
    )

    assert result["retCode"] == 110043
    assert result["retMsg"] == "leverage not changed"
    assert manager.client.send.call_count == 1


def test_p2p_method_is_available_on_unified_http(http, monkeypatch):
    captured = {}

    def fake_submit_request(**kwargs):
        captured.update(kwargs)
        return {"retCode": 0}

    monkeypatch.setattr(http, "_submit_request", fake_submit_request)

    result = http.get_ad_details(itemId="123")

    assert result == {"retCode": 0}
    assert captured == {
        "method": "POST",
        "path": "https://api-testnet.bybit.com/v5/p2p/item/info",
        "query": {"itemId": "123"},
        "auth": True,
    }


def test_upload_chat_file_is_available_on_unified_http(http, monkeypatch):
    captured = {}

    def fake_submit_file_request(**kwargs):
        captured.update(kwargs)
        return {"retCode": 0}

    monkeypatch.setattr(http, "_submit_file_request", fake_submit_file_request)

    result = http.upload_chat_file(upload_file=b"abc", filename="proof.png")

    assert result == {"retCode": 0}
    assert captured == {
        "path": "https://api-testnet.bybit.com/v5/p2p/oss/upload_file",
        "query": {"upload_file": b"abc", "filename": "proof.png"},
        "auth": True,
    }


def test_prepare_file_payload_supports_file_like_input():
    file = io.BytesIO(b"image-bytes")
    file.name = "receipt.png"

    body, content_type = _V5HTTPManager.prepare_file_payload(
        {"upload_file": file}
    )

    assert content_type == "multipart/form-data; boundary=boundary-for-file"
    assert b'name="upload_file"; filename="receipt.png"' in body
    assert b"Content-Type: image/png" in body
    assert b"image-bytes" in body


def test_prepare_headers_signs_binary_payload(monkeypatch):
    manager = _V5HTTPManager(api_key="mykey", api_secret="secret")
    body, content_type = _V5HTTPManager.prepare_file_payload(
        {"upload_file": b"abc", "filename": "proof.png"}
    )
    monkeypatch.setattr(
        "pybit._http_manager._helpers.generate_timestamp",
        lambda: 12345,
    )

    headers = manager._prepare_headers(
        body,
        recv_window=5000,
        content_type=content_type,
    )
    expected_signature = hmac.new(
        bytes("secret", "utf-8"),
        b"12345mykey5000" + body,
        hashlib.sha256,
    ).hexdigest()

    assert headers["Content-Type"] == content_type
    assert headers["X-BAPI-SIGN"] == expected_signature


def test_upload_chat_file_sends_multipart_request(monkeypatch):
    manager = HTTP(testnet=True, api_key=_api_key, api_secret=_api_secret)
    monkeypatch.setattr(
        "pybit._http_manager._helpers.generate_timestamp",
        lambda: 12345,
    )

    response = Mock()
    response.status_code = 200
    response.headers = {}
    response.elapsed = 0
    response.json.return_value = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {"url": "https://example.com/proof.png"},
        "time": 1234567890,
    }
    manager.client.send = Mock(return_value=response)

    result = manager.upload_chat_file(upload_file=b"abc", filename="proof.png")
    request = manager.client.send.call_args[0][0]

    assert result["retCode"] == 0
    assert request.method == "POST"
    assert request.url == (
        "https://api-testnet.bybit.com/v5/p2p/oss/upload_file"
    )
    assert request.headers["Content-Type"] == (
        "multipart/form-data; boundary=boundary-for-file"
    )
    assert b'name="upload_file"; filename="proof.png"' in request.body
    assert b"abc" in request.body
