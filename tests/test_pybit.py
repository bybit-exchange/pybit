"""Tests for the Pybit API wrapper."""

import sys
import inspect
import unittest
from unittest import mock
import time
from websocket import (
    WebSocketConnectionClosedException,
    WebSocketTimeoutException
)
from pybit.exceptions import (
    InvalidChannelTypeError,
    TopicMismatchError,
    NoCredentialsAuthorizationException
)
from pybit.unified_trading import HTTP, WebSocket
from pybit._utils import DEPRECATION_CONFIG

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
    def _callback_function(self, msg):
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
    def _callback_function(self, msg):
        print(msg)

    def test_private_websocket_connect(self):
        ws_private = WebSocket(
            testnet=True,
            channel_type="private",
            api_key="...",
            api_secret="...",
            trace_logging=True,
            # private_auth_expire=10
        )

        ws_private.position_stream(callback=self._callback_function)
        # time.sleep(10)


class WSOnErrorCallbackTest(unittest.TestCase):
    """ Test WebSocket on_error callback. """

    def test_tries_to_reconnect(self):
        """ Test if WebSocket tries to reconnect on connection error. """
        ws.restart_on_ws_disconnect = True
        ws.attempting_connection = False
        ws._reset = mock.MagicMock()
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        # WebSocketConnectionClosedException
        ws._on_error(ws, WebSocketConnectionClosedException())
        ws._reset.assert_called_once()
        ws._connect.assert_called_once()
        ws.exit.assert_called_once()
        # WebSocketTimeoutException
        ws._reset.reset_mock()
        ws._connect.reset_mock()
        ws.exit.reset_mock()
        ws._on_error(ws, WebSocketTimeoutException())
        ws._reset.assert_called_once()
        ws._connect.assert_called_once()
        ws.exit.assert_called_once()
    
    def test_doesnt_try_to_reconnect_when_restart_on_ws_disconnect_is_false(self):
        """ Test if WebSocket doesn't try to reconnect when restart_on_ws_disconnect is False. """
        ws.restart_on_ws_disconnect = False
        ws.attempting_connection = False
        ws._reset = mock.MagicMock()
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        self.assertRaises(
            WebSocketConnectionClosedException,
            ws._on_error, ws, WebSocketConnectionClosedException()
        )
        ws._reset.assert_not_called()
        ws._connect.assert_not_called()
        ws.exit.assert_called_once()

    def test_disconnects_on_pybit_exception(self):
        """ Test if WebSocket disconnects on Pybit exception. """
        ws.restart_on_ws_disconnect = False
        ws.attempting_connection = False
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        self.assertRaises(
            NoCredentialsAuthorizationException,
            ws._on_error, ws, NoCredentialsAuthorizationException()
        )
        ws._connect.assert_not_called()
        ws.exit.assert_called_once()
    
    def test_ignores_exceptions_when_disconnect_on_exception_is_false(self):
        """ Test if WebSocket ignores exceptions when disconnect_on_exception is False. """
        ws.disconnect_on_exception = False
        ws.restart_on_ws_disconnect = False
        ws.attempting_connection = False
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        ws._on_error(ws, Exception())
        ws._connect.assert_not_called()
        ws.exit.assert_not_called()
    
    def test_raises_exception_when_disconnect_on_exception_is_true(self):
        """ Test if WebSocket raises exception when disconnect_on_exception is True. """
        ws.disconnect_on_exception = True
        ws.restart_on_ws_disconnect = False
        ws.attempting_connection = False
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        self.assertRaises(
            Exception,
            ws._on_error, ws, Exception()
        )
        ws._connect.assert_not_called()
        ws.exit.assert_called_once()
    
    def test_doesn_nothing_when_attempting_connection_is_true(self):
        """ Test if WebSocket does nothing when attempting_connection is True. """
        ws.restart_on_ws_disconnect = True
        ws.attempting_connection = True
        ws._reset = mock.MagicMock()
        ws._connect = mock.MagicMock()
        ws.exit = mock.MagicMock()
        ws._on_error(ws, WebSocketConnectionClosedException())
        ws._reset.assert_not_called()
        ws._connect.assert_not_called()
        ws.exit.assert_not_called()


class DeprecatedMembersTest(unittest.TestCase):
    """ Test deprecated members. """

    def _check_deprecated_function(self, func):
        config = func.__dict__.get(DEPRECATION_CONFIG)
        if config and config.should_be_modified:
            message = (
                f'There are arguments from function "{config.function_name}" '
                'that are deprecated and must be removed in version '
                f'{config.modification_version}:\n' +
                ', '.join([f'"{x}"' for x in config.to_be_removed]) +
                (', ' if len(config.to_be_removed) > 0 else '') +
                ', '.join(
                    [f'"{x[0]}"(Replaced with "{x[1]}")' for x in config.to_be_replaced])
            )
            raise AssertionError(message)

    def _check_deprecated_class(self, cls):
        config = cls[1].__dict__.get(DEPRECATION_CONFIG)
        if config:
            self.assertFalse(
                config.should_be_modified,
                f'Class "{cls[0]}" should be removed in version {config.modification_version}!'
            )

    def test_should_modify_deprecated_members(self):
        """ Test if deprecated members(classes/functions) 
        should be modified(removed/renamed) in current version. 
        """
        pybit_modules = [e[1]
                         for e in sys.modules.items() if e[0].startswith('pybit.')]
        for module in pybit_modules:
            # Getting all classes from the module
            classes = inspect.getmembers(module, inspect.isclass)
            for cls in classes:
                # Check all classes in the module
                self._check_deprecated_class(cls)
                # Check all functions in the class
                for item in cls[1].__dict__.items():
                    if inspect.isfunction(item[1]):
                        self._check_deprecated_function(item[1])
            # Check all functions in the module
            functions = inspect.getmembers(module, inspect.isfunction)
            for func in functions:
                self._check_deprecated_function(func[1])
