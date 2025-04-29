import time
import unittest

from pybit.exceptions import InvalidChannelTypeError, TopicMismatchError
from pybit.unified_trading import HTTP, WebSocket

# session uses Bybit's mainnet endpoint
session = HTTP()
ws = WebSocket(
    channel_type="spot",
    testnet=False,
)


class HTTPTest(unittest.TestCase):
    def test_orderbook(self):
        self.assertEqual(
            session.get_orderbook(category="spot", symbol="BTCUSDT")["retMsg"],
            "OK",
        )

    def test_query_kline(self):
        self.assertEqual(
            (
                session.get_kline(
                    symbol="BTCUSDT",
                    interval="1",
                    from_time=int(time.time()) - 60 * 60,
                )["retMsg"]
            ),
            "OK",
        )

    def test_symbol_information(self):
        self.assertEqual(
            session.get_instruments_info(category="spot", symbol="BTCUSDT")[
                "retMsg"
            ],
            "OK",
        )

    # We can't really test authenticated endpoints without keys, but we
    # can make sure it raises a PermissionError.
    def test_place_active_order(self):
        with self.assertRaises(PermissionError):
            session.place_order(
                symbol="BTCUSD",
                order_type="Market",
                side="Buy",
                qty=1,
                category="spot",
            )


class WebSocketTest(unittest.TestCase):
    # A very simple test to ensure we're getting something from WS.
    def _callback_function(msg):
        print(msg)

    def test_websocket(self):
        self.assertNotEqual(
            ws.orderbook_stream(
                depth=1,
                symbol="BTCUSDT",
                callback=self._callback_function,
            ),
            [],
        )

    def test_invalid_category(self):
        with self.assertRaises(InvalidChannelTypeError):
            WebSocket(
                channel_type="not_exists",
                testnet=False,
            )

    def test_topic_category_mismatch(self):
        with self.assertRaises(TopicMismatchError):
            ws = WebSocket(
                channel_type="linear",
                testnet=False,
            )

            ws.order_stream(callback=self._callback_function)
            
class PrivateWebSocketTest(unittest.TestCase):
    # Connect to private websocket and see if we can auth.
    def _callback_function(msg):
        print(msg)
    
    def test_private_websocket_connect(self):
        ws_private = WebSocket(
            testnet=True,
            channel_type="private",
            api_key="...",
            api_secret="...",
            trace_logging=True,
            #private_auth_expire=10
        )
        
        ws_private.position_stream(callback=self._callback_function)
        #time.sleep(10)
