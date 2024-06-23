""" Websocket stream manager for Bybit API. """

from typing import Optional, Union, Callable
import threading
import time
import json
import logging
import copy
from uuid import uuid4
import websocket
from ._http_manager import generate_signature
from .exceptions import (
    PybitException,
    AlreadySubscribedTopicException,
    AuthorizationFailedException,
    WSConnectionNotEstablishedException
)
from ._utils import deprecate_function_arguments
from . import _helpers


logger = logging.getLogger(__name__)


SUBDOMAIN_TESTNET = "stream-testnet"
SUBDOMAIN_MAINNET = "stream"
DEMO_SUBDOMAIN_TESTNET = "stream-demo-testnet"
DEMO_SUBDOMAIN_MAINNET = "stream-demo"
DOMAIN_MAIN = "bybit"
DOMAIN_ALT = "bytick"


class _WebSocketManager:
    ws: Optional[websocket.WebSocketApp]
    wst: Optional[threading.Thread]
    auth: bool
    exited: bool
    attempting_connection: bool
    data: dict

    @deprecate_function_arguments(
        "6.0",
        to_be_replaced=("restart_on_error", "restart_on_ws_disconnect"),
    )
    def __init__(
        self,
        callback_function,
        ws_name,
        testnet,
        domain="",
        demo=False,
        rsa_authentication=False,
        api_key=None,
        api_secret=None,
        ping_interval=20,
        ping_timeout=10,
        retries=10,
        restart_on_error: Optional[bool] = None,
        restart_on_ws_disconnect: bool = True,
        disconnect_on_exception: bool = True,
        trace_logging=False,
        private_auth_expire=1,
        skip_utf8_validation=True,
    ):
        self.testnet = testnet
        self.domain = domain
        self.rsa_authentication = rsa_authentication
        self.demo = demo
        # Set API keys.
        self.api_key = api_key
        self.api_secret = api_secret

        self.callback = callback_function
        self.ws_name = ws_name
        if api_key:
            self.ws_name += " (Auth)"

        # Delta time for private auth expiration in seconds
        self.private_auth_expire = private_auth_expire

        # Setup the callback directory following the format:
        #   {
        #       "topic_name": function
        #   }
        self.callback_directory: dict[str, Callable] = {}

        # Record the subscriptions made so that we can resubscribe if the WSS
        # connection is broken.
        self.subscriptions: dict[str, str] = {}

        # Set ping settings.
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.custom_ping_message = json.dumps({"op": "ping"})
        self.retries = retries

        # Other optional data handling settings.
        self.restart_on_ws_disconnect = restart_on_error or restart_on_ws_disconnect
        # If True, disconnects the websocket connection when a non-websocket
        # exception is raised(for example, a broken ws message was received, which
        # caused wrong handling, and, therefore, an exception was thrown).
        # If False, the websocket connection will not be closed, and the exception
        # will be ignored(will be only logged).
        self.disconnect_on_exception = disconnect_on_exception

        # Enable websocket-client's trace logging for extra debug information
        # on the websocket connection, including the raw sent & recv messages
        websocket.enableTrace(trace_logging)

        # Set the skip_utf8_validation parameter to True to skip the utf-8
        # validation of incoming messages.
        # Could be useful if incoming messages contain invalid utf-8 characters.
        # Also disabling utf-8 validation could improve performance
        # (more about performance: https://github.com/websocket-client/websocket-client).
        self.skip_utf8_validation = skip_utf8_validation

        # Set initial state, initialize dictionary and connect.
        self.auth = False
        self.exited = False
        self.data = {}
        self.endpoint = None
        self.ws = None
        self.wst = None
        self.attempting_connection = False

    def _on_open(self, *_):
        """
        Log WS open.
        """
        logger.debug("WebSocket %s opened.", self.ws_name)

    def _on_message(self, _, message):
        """
        Parse incoming messages.
        """
        message = json.loads(message)
        if self._is_custom_pong(message):
            return
        else:
            self.callback(message)

    def is_connected(self):
        """ Check if the websocket is connected. """
        try:
            if self.ws.sock.connected:
                return True
            else:
                return False
        except AttributeError:
            return False

    def _send(self, message):
        if self.ws is None:
            raise WSConnectionNotEstablishedException()
        self.ws.send(message)

    def _connect(self, url):
        """
        Open websocket in a thread.
        """

        def resubscribe_to_topics():
            if not self.subscriptions:
                # There are no subscriptions to resubscribe to, probably
                # because this is a brand new WSS initialisation so there was
                # no previous WSS connection.
                return

            for _, subscription_message in self.subscriptions.items():
                self._send(subscription_message)

        self.attempting_connection = True

        # Set endpoint.
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        domain = DOMAIN_MAIN if not self.domain else self.domain
        if self.demo:
            if self.testnet:
                subdomain = DEMO_SUBDOMAIN_TESTNET
            else:
                subdomain = DEMO_SUBDOMAIN_MAINNET
        url = url.format(SUBDOMAIN=subdomain, DOMAIN=domain)
        self.endpoint = url

        # Attempt to connect for X seconds.
        retries = self.retries
        if retries == 0:
            infinitely_reconnect = True
        else:
            infinitely_reconnect = False

        while (
            infinitely_reconnect or retries > 0
        ) and not self.is_connected():
            logger.info("WebSocket %s attempting connection...", self.ws_name)
            self.ws = websocket.WebSocketApp(
                url=url,
                on_message=self._on_message,
                on_close=self._on_close,
                on_open=self._on_open,
                on_error=self._on_error,
                on_pong=self._on_pong,
            )

            # Setup the thread running WebSocketApp.
            self.wst = threading.Thread(
                target=lambda: self.ws.run_forever(
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout,
                    skip_utf8_validation=self.skip_utf8_validation,
                )
            )

            # Configure as daemon; start.
            self.wst.daemon = True
            self.wst.start()

            retries -= 1
            while self.wst.is_alive():
                if self.ws.sock and self.is_connected():
                    break

            # If connection was not successful, raise error.
            if not infinitely_reconnect and retries <= 0:
                self.exit()
                raise websocket.WebSocketTimeoutException(
                    f"WebSocket {self.ws_name} ({self.endpoint}) connection "
                    "failed. Too many connection attempts. pybit will no "
                    "longer try to reconnect."

                )

        logger.info("WebSocket %s connected", self.ws_name)

        # If given an api_key, authenticate.
        if self.api_key and self.api_secret:
            self._auth()

        resubscribe_to_topics()
        self._send_initial_ping()

        self.attempting_connection = False

    def _auth(self):
        """
        Prepares authentication signature per Bybit API specifications.
        """

        expires = _helpers.generate_timestamp() + (self.private_auth_expire * 1000)

        param_str = f"GET/realtime{expires}"

        signature = generate_signature(
            self.rsa_authentication, self.api_secret, param_str
        )

        # Authenticate with API.
        self._send(
            json.dumps(
                {"op": "auth", "args": [self.api_key, expires, signature]}
            )
        )

    def _on_error(self, _, error):
        """
        Exit on errors and raise exception, or attempt reconnect.
        """
        is_ws_disconnect = any(
            map(
                lambda exception: isinstance(error, exception),
                [
                    websocket.WebSocketConnectionClosedException,
                    websocket.WebSocketTimeoutException,
                ]
            )
        )
        should_raise = isinstance(error, PybitException) or \
            (is_ws_disconnect and not self.restart_on_ws_disconnect) or \
            (not is_ws_disconnect and self.disconnect_on_exception)

        log_callback = logger.error if is_ws_disconnect else logger.exception
        log_callback(
            "WebSocket %(ws_name)s (%(endpoint)s) encountered error: %(error)s.",
            {"ws_name": self.ws_name, "endpoint": self.endpoint, "error": error},
        )

        if is_ws_disconnect and self.restart_on_ws_disconnect and not self.attempting_connection:
            if not self.exited:
                self.exit()
            logger.info(
                "Attempting to reconnect WebSocket %s...",
                self.ws_name
            )
            self._reset()
            self._connect(self.endpoint)

        if should_raise:
            self.exit()
            logger.info(
                "WebSocket %s closed because an exception was raised."
                "If you want to keep the connection open, set disconnect_on_exception=False",
                self.ws_name
            )
            raise error

    def _on_close(self, *args):
        """
        Log WS close.
        """
        logger.debug("WebSocket %s closed.", self.ws_name)

    def _on_pong(self, *args):
        """
        Sends a custom ping upon the receipt of the pong frame.

        The websocket library will automatically send ping frames. However, to
        ensure the connection to Bybit stays open, we need to send a custom
        ping message separately from this. When we receive the response to the
        ping frame, this method is called, and we will send the custom ping as
        a normal OPCODE_TEXT message and not an OPCODE_PING.
        """
        self._send_custom_ping()

    def _send_custom_ping(self):
        self._send(self.custom_ping_message)

    def _send_initial_ping(self):
        """https://github.com/bybit-exchange/pybit/issues/164"""
        timer = threading.Timer(
            self.ping_interval, self._send_custom_ping
        )
        timer.start()

    @staticmethod
    def _is_custom_pong(message):
        """
        Referring to OPCODE_TEXT pongs from Bybit, not OPCODE_PONG.
        """
        if message.get("ret_msg") == "pong" or message.get("op") == "pong":
            return True

    def _reset(self):
        """
        Set state booleans and initialize dictionary.
        """
        self.exited = False
        self.auth = False
        self.data = {}

    def exit(self):
        """
        Closes the websocket connection.
        """

        self.ws.close()
        while self.ws.sock:
            continue
        self.exited = True


class _V5WebSocketManager(_WebSocketManager):
    def __init__(self, ws_name, **kwargs):
        callback_function = (
            kwargs.pop("callback_function")
            if kwargs.get("callback_function")
            else self._handle_incoming_message
        )
        super().__init__(callback_function, ws_name, **kwargs)

        self.subscriptions = {}

        self.private_topics = [
            "position",
            "execution",
            "order",
            "wallet",
            "greeks",
        ]

    def subscribe(
            self,
            topic: str,
            callback,
            symbol: Union[str, list[str], None] = None,
    ):
        """ Subscribe to a topic on the websocket stream. """
        symbol = symbol or []

        def prepare_subscription_args(list_of_symbols):
            """
            Prepares the topic for subscription by formatting it with the
            desired symbols.
            """

            if topic in self.private_topics:
                # private topics do not support filters
                return [topic]

            topics = []
            for single_symbol in list_of_symbols:
                topics.append(topic.format(symbol=single_symbol))
            return topics

        if isinstance(symbol, str):
            symbol = [symbol]

        subscription_args = prepare_subscription_args(symbol)
        self._check_callback_directory(subscription_args)

        req_id = str(uuid4())

        subscription_message = json.dumps(
            {"op": "subscribe", "req_id": req_id, "args": subscription_args}
        )
        while not self.is_connected():
            # Wait until the connection is open before subscribing.
            time.sleep(0.1)
        self._send(subscription_message)
        self.subscriptions[req_id] = subscription_message
        for topic in subscription_args:
            self._set_callback(topic, callback)

    def _initialise_local_data(self, topic):
        # Create self.data
        try:
            self.data[topic]
        except KeyError:
            self.data[topic] = []

    def _process_delta_orderbook(self, message, topic):
        self._initialise_local_data(topic)

        # Record the initial snapshot.
        if "snapshot" in message["type"]:
            self.data[topic] = message["data"]
            return

        # Make updates according to delta response.
        book_sides = {"b": message["data"]["b"], "a": message["data"]["a"]}
        self.data[topic]["u"] = message["data"]["u"]
        self.data[topic]["seq"] = message["data"]["seq"]

        for side, entries in book_sides.items():
            for entry in entries:
                # Delete.
                if float(entry[1]) == 0:
                    index = _helpers.find_index(
                        self.data[topic][side], entry, 0
                    )
                    self.data[topic][side].pop(index)
                    continue

                # Insert.
                price_level_exists = entry[0] in [
                    level[0] for level in self.data[topic][side]
                ]
                if not price_level_exists:
                    self.data[topic][side].append(entry)
                    continue

                # Update.
                qty_changed = entry[1] != next(
                    level[1]
                    for level in self.data[topic][side]
                    if level[0] == entry[0]
                )
                if price_level_exists and qty_changed:
                    index = _helpers.find_index(
                        self.data[topic][side], entry, 0
                    )
                    self.data[topic][side][index] = entry
                    continue

    def _process_delta_ticker(self, message, topic):
        self._initialise_local_data(topic)

        # Record the initial snapshot.
        if "snapshot" in message["type"]:
            self.data[topic] = message["data"]

        # Make updates according to delta response.
        elif "delta" in message["type"]:
            for key, value in message["data"].items():
                self.data[topic][key] = value

    def _process_auth_message(self, message):
        # If we get successful futures auth, notify user
        if message.get("success") is True:
            logger.debug("Authorization for %s successful.", self.ws_name)
            self.auth = True
        # If we get unsuccessful auth, notify user.
        elif message.get("success") is False or message.get("type") == "error":
            raise AuthorizationFailedException(
                ws_name=self.ws_name,
                raw_message=message,
            )

    def _process_subscription_message(self, message):
        if message.get("req_id"):
            sub = self.subscriptions[message["req_id"]]
        else:
            # if req_id is not supported, guess that the last subscription
            # sent was successful
            sub = json.loads(list(self.subscriptions.items())[0][1])["args"][0]

        # If we get successful futures subscription, notify user
        if message.get("success") is True:
            logger.debug("Subscription to %s successful.", sub)
        # Futures subscription fail
        elif message.get("success") is False:
            response = message["ret_msg"]
            logger.error("Couldn't subscribe to topic. Error: %s.", response)
            self._pop_callback(sub[0])

    def _process_normal_message(self, message):
        topic = message["topic"]
        if "orderbook" in topic:
            self._process_delta_orderbook(message, topic)
            callback_data = copy.deepcopy(message)
            callback_data["type"] = "snapshot"
            callback_data["data"] = self.data[topic]
        elif "tickers" in topic:
            self._process_delta_ticker(message, topic)
            callback_data = copy.deepcopy(message)
            callback_data["type"] = "snapshot"
            callback_data["data"] = self.data[topic]
        else:
            callback_data = message
        callback_function = self._get_callback(topic)
        callback_function(callback_data)

    def _handle_incoming_message(self, message):
        def is_auth_message():
            if (
                message.get("op") == "auth"
                or message.get("type") == "AUTH_RESP"
            ):
                return True
            else:
                return False

        def is_subscription_message():
            if (
                message.get("op") == "subscribe"
                or message.get("type") == "COMMAND_RESP"
            ):
                return True
            else:
                return False

        if is_auth_message():
            self._process_auth_message(message)
        elif is_subscription_message():
            self._process_subscription_message(message)
        else:
            self._process_normal_message(message)

    def _check_callback_directory(self, topics):
        for topic in topics:
            if topic in self.callback_directory:
                raise AlreadySubscribedTopicException(topic)

    def _set_callback(self, topic, callback_function):
        self.callback_directory[topic] = callback_function

    def _get_callback(self, topic):
        return self.callback_directory[topic]

    def _pop_callback(self, topic):
        self.callback_directory.pop(topic)
