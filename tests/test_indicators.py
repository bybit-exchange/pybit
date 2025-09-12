import pytest
from pybit import HTTP, Indicators

def test_get_momentum(monkeypatch):
    # Mock HTTP client
    class MockHTTP:
        def get_kline(self, **kwargs):
            return {
                "result": {
                    "list": [
                        ["t", "100", "110", "90", "100", "10"],
                        ["t", "101", "111", "91", "105", "10"],
                    ]
                }
            }

    client = MockHTTP()
    indicators = Indicators(client)
    momentum = indicators.get_momentum("BTCUSDT", interval="60", lookback=1)
    assert momentum == 5.0
