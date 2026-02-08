import websocket
import threading
import time
import json
from ._http_manager import generate_signature
import logging
import copy
from typing import Callable, Any
from uuid import uuid4
from . import _helpers

from .models.reconnector import Reconnector, FixedDelay, LinearBackoff


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
        trace_logging=False,
        private_auth_expire=1,
        recconnect_attempts=-1,
        reconnector: Reconnector = LinearBackoff(5, 60),
        on_message: Callable[[Any], None] | None=None,
        on_reconnect: Callable[[], None] | None=None
    ):
        """
            recnnect_attempts: number of times to try reconnecting each time websocket closes
                -1 means infinite attempts
        """

        self.testnet = testnet
        self.domain = domain
        self.tld = tld
        self.rsa_authentication = rsa_authentication
        self.demo = demo
        # Set API keys.
        self.api_key = api_key
        self.api_secret = api_secret

        self.on_message = on_message
        self.ws_name = ws_name
        if api_key:
            self.ws_name += " (Auth)"
        
        # Delta time for private auth expiration in seconds
        self.private_auth_expire = private_auth_expire

        self.reconnect_attempts=recconnect_attempts
        self.reconnector = reconnector
        self.on_reconnect = on_reconnect

        # Setup the callback directory following the format:
        #   {
        #       "topic_name": function
        #   }
        self.callback_directory = {}

        # Record the subscriptions made so that we can resubscribe if the WSS
        # connection is broken.
        self.subscriptions = {}

        # Set ping settings.
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.custom_ping_message = json.dumps({"op": "ping"})

        # Enable websocket-client's trace logging for extra debug information
        # on the websocket connection, including the raw sent & recv messages
        websocket.enableTrace(trace_logging)

        # threads and shared states
        self.started = threading.Event()
        self.connected = threading.Event()
        self.reconnecting = threading.Event()
        self.ws_thread = None
        self.reconnect_thread = threading.Thread(target=self.reconnect_loop, daemon=True)

    def start(self, url: str):

        if self.started.is_set():
            logger.warning(f"Websocket {self.ws_name} is already connected.")
            return
        
        self._connect(url)
            
        self.started.set()
        logger.info(f"Websocket {self.ws_name} started")
        if not self.reconnect_thread or not self.reconnect_thread.is_alive():
            self.reconnect_thread.start()

    def _connect(self, url: str):
        self._dial(url)   

        # If given an api_key, authenticate.
        if self.api_key and self.api_secret:
            self._auth()

        def resubscribe_to_topics():
            if not self.subscriptions:
                # There are no subscriptions to resubscribe to, probably
                # because this is a brand new WSS initialisation so there was
                # no previous WSS connection.
                return

            for subscription_message in self.subscriptions.values():
                self.ws.send(subscription_message)
                
        resubscribe_to_topics()
        self._send_initial_ping()

    def _dial(self, url: str):
        """ Raise Exception if websocket doesn't connect after 10 secs"""
        
        # Set endpoint.
        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        domain = DOMAIN_MAIN if not self.domain else self.domain
        tld = TLD_MAIN if not self.tld else self.tld
        if self.demo:
            if self.testnet:
                subdomain = DEMO_SUBDOMAIN_TESTNET
            else:
                subdomain = DEMO_SUBDOMAIN_MAINNET
        self.endpoint = url.format(SUBDOMAIN=subdomain, DOMAIN=domain, TLD=tld)

        self.ws = websocket.WebSocketApp(
            url=self.endpoint,
            on_message=self._on_message,
            on_close=self._on_close,
            on_open=self._on_open,
            on_error=self._on_error,
            on_pong=self._on_pong,
        )
        if not self.ws_thread or not self.ws_thread.is_alive():
            self.ws_thread = threading.Thread(
                target=lambda: self.ws.run_forever(
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout,
                ), 
                daemon=True
            )
            self.ws_thread.start()
        
        if not self.connected.wait(timeout=10):
            self.ws.close()
            raise Exception(f"Websocket {self.ws_name} Failed to connect")
    
    def reconnect_loop(self):
        logger.info(f"Websocket {self.ws_name} Reconnecting loop started")
        while self.started.is_set():
            if self.reconnecting.is_set():
                try:
                    attempts = 0                    
                    while (
                        (self.reconnect_attempts == -1) or 
                        (attempts < self.reconnect_attempts)
                    ):
                        interval = None
                        if isinstance(self.reconnector, FixedDelay):
                            interval = self.reconnector.get_interval()
                        else:
                            interval = self.reconnector.get_interval(attempts+1)

                        logger.info(
                            f"Websocket {self.ws_name} Reconnecting in {interval} seconds... (attempt {attempts+1})")
                                
                        time.sleep(interval)
                        try:
                            self._connect(self.endpoint)
                            if self.on_reconnect:
                                self.on_reconnect()
                            logger.info(f"Websocket {self.ws_name} Reconnect Success")
                            break
                        except Exception as e:
                            attempts += 1
                            logger.error(f"Websocket {self.ws_name} Reconnect attempt {attempts} failed: {e}")
                finally:
                    self.reconnecting.clear()
            time.sleep(1)
        logger.info(f"Websocket {self.ws_name} Exiting reconnect loop...")

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

    def _on_open(self, ws):
        """
        Log WS open.
        """
        logger.debug(f"WebSocket {self.ws_name} opened.")
        self.connected.set()

    def _on_message(self, ws, message):
        """
        Parse incoming messages.
        """
        message = json.loads(message)
        if self._is_custom_pong(message):
            return
        else:
            if self.on_message:
                self.on_message(message)

    def _on_error(self, ws, error):
        logger.error(f"WebSocket {self.ws_name} error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket {self.ws_name} closed with status code {close_status_code}, message: {close_msg}")
        self.connected.clear()
        if not self.started.is_set():
            return
        self.reconnecting.set()

    def _on_pong(self, ws, *args):
        """
        Sends a custom ping upon the receipt of the pong frame.

        The websocket library will automatically send ping frames. However, to
        ensure the connection to Bybit stays open, we need to send a custom
        ping message separately from this. When we receive the response to the
        ping frame, this method is called, and we will send the custom ping as
        a normal OPCODE_TEXT message and not an OPCODE_PING.
        """
        try:
            self._send_custom_ping()
        except:
            logger.error("Error sending ping")
            raise

    def _send_custom_ping(self):
        if self.connected.is_set():
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
        
    def stop(self):
        """Close websocket connection and update related states"""
        self.started.clear()
        self.ws.close()
        if self.ws_thread:
            self.ws_thread.join()
        self.reconnect_thread.join()
        logger.info(f"WebSocket {self.ws_name} stopped.")


class _V5WebSocketManager(_WebSocketManager):
    def __init__(self, ws_name, **kwargs):
        callback_function = (
            kwargs.pop("callback_function")
            if kwargs.get("callback_function")
            else self._handle_incoming_message
        )
        super().__init__(ws_name=ws_name, on_message=callback_function, **kwargs)

        self.standard_private_topics = [
            "position",
            "execution",
            "order",
            "wallet",
            "greeks",
            "spread.order",
            "spread.execution",
        ]

        self.other_private_topics = [
            "execution.fast"
        ]

        self.standard_public_topics = [
            "system.status",
        ]

        self.data = {}

    def subscribe(
        self,
        topic: str,
        callback,
        symbol: str | list=[]
    ):

        def prepare_subscription_args(list_of_symbols):
            """
            Prepares the topic for subscription by formatting it with the
            desired symbols.
            """

            if topic in self.standard_private_topics + self.standard_public_topics:
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
        
        if not self.connected.wait(timeout=10):
            logger.warning("Unable to send subscription messaged. WS client not connected!")
            return

        self.ws.send(subscription_message)
        self.subscriptions[req_id] = subscription_message
        for topic in subscription_args:
            self._set_callback(topic, callback)

    def unsubscribe(self, topic: str):

        """
        Unsubscribe from a given topic.

        This method searches the active subscriptions for the specified topic,
        constructs an unsubscribe message, and sends it through the WebSocket
        connection.
        """

        sub = None
        for _,value in self.subscriptions.items(): # Find subscribe message
            if topic in value:
                sub=value
                break

        if sub:
            # The original `req_id` from the subscription message is intentionally
            # left unchanged. Only the `"op"` field is updated to `"unsubscribe"`.
            # This ensures that when the server responds, it uses the same `req_id`,
            # allowing `_process_unsubscription_message` to correctly identify and
            # remove the corresponding subscription.
       
            unsub_message = json.loads(sub)
            unsub_message["op"] = "unsubscribe"

            self.ws.send(json.dumps(unsub_message))
            logger.debug("Unsubscribe request sent for topic: %s", topic)
        else:
            logger.error("Couldn't find active subscription for topic: %s", topic)

    def get_subscription_topics(self):
        """
        Retrieve all subscribed topics.

        Returns:
            list[str]: A list of topic strings that the client is currently subscribed to.
        """
        topics = []
        subscription_values = list(self.subscriptions.values())

        for subscription in subscription_values:
            data = json.loads(subscription)

            for topic in data["args"]:
                topics.append(topic)

        return topics

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
        # If we get unsuccessful auth, notify user.
        elif message.get("success") is False or message.get("type") == "error":
            raise Exception(
                f"Authorization for {self.ws_name} failed. Please check your "
                f"API keys and resync your system time. Raw error: {message}"
            )

    def _process_subscription_message(self, message):
        if message.get("req_id"):
            topic = self.subscriptions[message["req_id"]]
        else:
            # if req_id is not supported, guess that the last subscription
            # sent was successful
            topic = json.loads(list(self.subscriptions.items())[0][1])["args"][0]

        # If we get successful futures subscription, notify user
        if message.get("success") is True:
            logger.debug(f"Subscription to {topic} successful.")
        # Futures subscription fail
        elif message.get("success") is False:
            response = message["ret_msg"]
            logger.error("Couldn't subscribe to topic." f"Error: {response}.")
            self._pop_callback(topic[0])

    def _process_unsubscription_message(self,message):
        if message.get("req_id"):
            if message.get("success") is True and message["req_id"] in self.subscriptions:
                topic = json.loads(self.subscriptions[message["req_id"]])["args"][0]
                self.subscriptions.pop(message["req_id"]) # Remove from active subscriptions
                self._pop_callback(topic) # Remove topic from callbacks
                logger.debug(f"Unsubscription from {topic} successful.")
            else:
                logger.error("Unsubscription for request_id '%s' failed. Message: %s", message["req_id"], message)

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
        def is_unsubscription_message():
            if message.get("op") == "unsubscribe":
                return True
            else:
                return False

        if is_auth_message():
            self._process_auth_message(message)
        elif is_subscription_message():
            self._process_subscription_message(message)
        elif is_unsubscription_message():
            self._process_unsubscription_message(message)
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
