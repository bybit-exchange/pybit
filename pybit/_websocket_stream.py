import websocket
import threading
import time
import json
from ._http_manager import generate_signature
import logging
import copy
from uuid import uuid4
from . import _helpers


logger = logging.getLogger(__name__)


SUBDOMAIN_TESTNET = "stream-testnet"
SUBDOMAIN_MAINNET = "stream"
DEMO_SUBDOMAIN_TESTNET = "stream-demo-testnet"
DEMO_SUBDOMAIN_MAINNET = "stream-demo"
DOMAIN_MAIN = "bybit"
DOMAIN_ALT = "bytick"
TLD_MAIN = "com"


class _WebSocketManager:
    def __init__(
        self,
        _callback_function,
        ws_name,
        testnet,
        tld="",
        domain="",
        demo=False,
        rsa_authentication=False,
        api_key=None,
        api_secret=None,
        ping_interval=20,
        ping_timeout=10,
        retries=10,
        restart_on_error=True,
        trace_logging=False,
        private_auth_expire=1,
    ):
        self.testnet = testnet
        self.domain = domain
        self.tld = tld
        self.rsa_authentication = rsa_authentication
        self.demo = demo
        # Set API keys.
        self.api_key = api_key
        self.api_secret = api_secret

        self.callback = _callback_function
        self.ws_name = ws_name
        if api_key:
            self.ws_name += " (Auth)"
        
        # Delta time for private auth expiration in seconds
        self.private_auth_expire = private_auth_expire

        # Setup the callback directory following the format:
        #   {
        #       "topic_name": function
        #   }
        self.callback_directory = {}

        # Record the subscriptions made so that we can resubscribe if the WSS
        # connection is broken.
        self.subscriptions = []

        # Set ping settings.
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.custom_ping_message = json.dumps({"op": "ping"})
        self.retries = retries

        # Other optional data handling settings.
        self.handle_error = restart_on_error

        # Enable websocket-client's trace logging for extra debug information
        # on the websocket connection, including the raw sent & recv messages
        websocket.enableTrace(trace_logging)

        # Set initial state, initialize dictionary and connect.
        self._reset()
        self.attempting_connection = False

    def _on_open(self):
        """
        Log WS open.
        """
        logger.debug(f"WebSocket {self.ws_name} opened.")

    def _on_message(self, message):
        """
        Parse incoming messages.
        """
        message = json.loads(message)
        if self._is_custom_pong(message):
            return
        else:
            self.callback(message)

    def is_connected(self):
        try:
            if self.ws.sock.connected:
                return True
            else:
                return False
        except AttributeError:
            return False

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

            for req_id, subscription_message in self.subscriptions.items():
                self.ws.send(subscription_message)

        self.attempting_connection = True

        # Set endpoint.
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        domain = DOMAIN_MAIN if not self.domain else self.domain
        tld = TLD_MAIN if not self.tld else self.tld
        if self.demo:
            if self.testnet:
                subdomain = DEMO_SUBDOMAIN_TESTNET
            else:
                subdomain = DEMO_SUBDOMAIN_MAINNET
        url = url.format(SUBDOMAIN=subdomain, DOMAIN=domain, TLD=tld)
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
            logger.info(f"WebSocket {self.ws_name} attempting connection...")
            self.ws = websocket.WebSocketApp(
                url=url,
                on_message=lambda ws, msg: self._on_message(msg),
                on_close=lambda ws, *args: self._on_close(),
                on_open=lambda ws, *args: self._on_open(),
                on_error=lambda ws, err: self._on_error(err),
                on_pong=lambda ws, *args: self._on_pong(),
            )

            # Setup the thread running WebSocketApp.
            self.wst = threading.Thread(
                target=lambda: self.ws.run_forever(
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout,
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
                    f"failed. Too many connection attempts. pybit will no "
                    f"longer try to reconnect."
                )

        logger.info(f"WebSocket {self.ws_name} connected")

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
        self.ws.send(
            json.dumps(
                {"op": "auth", "args": [self.api_key, expires, signature]}
            )
        )

    def _on_error(self, error):
        """
        Exit on errors and raise exception, or attempt reconnect.
        """
        if type(error).__name__ not in [
            "WebSocketConnectionClosedException",
            "ConnectionResetError",
            "WebSocketTimeoutException",
        ]:
            # Raises errors not related to websocket disconnection.
            self.exit()
            raise error

        if not self.exited:
            logger.error(
                f"WebSocket {self.ws_name} ({self.endpoint}) "
                f"encountered error: {error}."
            )
            self.exit()

        # Reconnect.
        if self.handle_error and not self.attempting_connection:
            self._reset()
            self._connect(self.endpoint)

    def _on_close(self):
        """
        Log WS close.
        """
        logger.debug(f"WebSocket {self.ws_name} closed.")

    def _on_pong(self):
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
        self.ws.send(self.custom_ping_message)

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

        self.standard_private_topics = [
            "position",
            "execution",
            "order",
            "wallet",
            "greeks",
        ]

        self.other_private_topics = [
            "execution.fast"
        ]

    def subscribe(
            self,
            topic: str,
            callback,
            symbol: (str, list) = False
    ):

        def prepare_subscription_args(list_of_symbols):
            """
            Prepares the topic for subscription by formatting it with the
            desired symbols.
            """

            if topic in self.standard_private_topics:
                # private topics do not support filters
                return [topic]

            topics = []
            for single_symbol in list_of_symbols:
                topics.append(topic.format(symbol=single_symbol))
            return topics

        if type(symbol) == str:
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
        self.ws.send(subscription_message)
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
        self.data[topic]["u"]=message["data"]["u"]
        self.data[topic]["seq"]=message["data"]["seq"]

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
            logger.debug(f"Authorization for {self.ws_name} successful.")
            self.auth = True
        # If we get unsuccessful auth, notify user.
        elif message.get("success") is False or message.get("type") == "error":
            raise Exception(
                f"Authorization for {self.ws_name} failed. Please check your "
                f"API keys and resync your system time. Raw error: {message}"
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
            logger.debug(f"Subscription to {sub} successful.")
        # Futures subscription fail
        elif message.get("success") is False:
            response = message["ret_msg"]
            logger.error("Couldn't subscribe to topic." f"Error: {response}.")
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
                raise Exception(
                    f"You have already subscribed to this topic: " f"{topic}"
                )

    def _set_callback(self, topic, callback_function):
        self.callback_directory[topic] = callback_function

    def _get_callback(self, topic):
        return self.callback_directory[topic]

    def _pop_callback(self, topic):
        self.callback_directory.pop(topic)
