"""Module for the WebSocket Trading API."""

import json
import uuid
import logging
from ._websocket_stream import _WebSocketManager
from . import _helpers
from .exceptions import AuthorizationFailedException


logger = logging.getLogger(__name__)


WSS_NAME = "WebSocket Trading"
TRADE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/v5/trade"


class _V5TradeWebSocketManager(_WebSocketManager):
    def __init__(self, recv_window, referral_id, **kwargs):
        super().__init__(self._handle_incoming_message, WSS_NAME, **kwargs)
        self.recv_window = recv_window
        self.referral_id = referral_id
        self._connect(TRADE_WSS)

    def _process_auth_message(self, message):
        # If we get successful auth, notify user
        if message.get("retCode") == 0:
            logger.debug("Authorization for %s successful.", self.ws_name)
            self.auth = True
        # If we get unsuccessful auth, notify user.
        else:
            raise AuthorizationFailedException(
                raw_message=message,
                ws_name=self.ws_name,
            )

    def _process_error_message(self, message):
        logger.error(
            "WebSocket request %s hit an error. Enabling "
            "traceLogging to reproduce the issue. Raw error: %s",
            message['reqId'],
            message,

        )
        self._pop_callback(message["reqId"])

    def _handle_incoming_message(self, message):
        if message.get("op") == "auth":
            self._process_auth_message(message)
        elif message.get("retCode") != 0:
            self._process_error_message(message)
        else:
            callback_function = self._pop_callback(message["reqId"])
            callback_function(message)

    def _set_callback(self, topic, callback_function):
        self.callback_directory[topic] = callback_function

    def _pop_callback(self, topic):
        return self.callback_directory.pop(topic)

    def _send_order_operation(self, operation, callback, request):
        request_id = str(uuid.uuid4())

        message = {
            "reqId": request_id,
            "header": {
                "X-BAPI-TIMESTAMP": _helpers.generate_timestamp(),
            },
            "op": operation,
            "args": [
                request
            ],
        }

        if self.recv_window:
            message["header"]["X-BAPI-RECV-WINDOW"] = self.recv_window
        if self.referral_id:
            message["header"]["Referer"] = self.referral_id

        self.ws.send(json.dumps(message))
        self._set_callback(request_id, callback)
