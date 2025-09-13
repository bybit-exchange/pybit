import logging

import pytest
import hmac
import hashlib
from collections import defaultdict

import requests

from pybit._http_manager import _V5HTTPManager
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
