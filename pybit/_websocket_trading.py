from dataclasses import dataclass, field
import json
import uuid
import logging
from ._websocket_stream import _WebSocketManager
from . import _helpers


logger = logging.getLogger(__name__)


WSS_NAME = "WebSocket Trading"
TRADE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.{TLD}/v5/trade"


class _V5TradeWebSocketManager(_WebSocketManager):
    def __init__(self, recv_window, referral_id, **kwargs):
        super().__init__(self._handle_incoming_message, WSS_NAME, **kwargs)
        self.recv_window = recv_window
        self.referral_id = referral_id
        self._connect(TRADE_WSS)

    def _process_auth_message(self, message):
        # If we get successful auth, notify user
        if message.get("retCode") == 0:
            logger.debug(f"Authorization for {self.ws_name} successful.")
            self.auth = True
        # If we get unsuccessful auth, notify user.
        else:
            raise Exception(
                f"Authorization for {self.ws_name} failed. Please check your "
                f"API keys and resync your system time. Raw error: {message}"
            )

    def _handle_incoming_message(self, message):
        if message.get("op") == "auth":
            self._process_auth_message(message)
            return

        req_id = message.get("reqId")
        callback, error_callback = self._pop_callback(req_id)

        if message.get("retCode") != 0:
            logger.warning(
                f"WebSocket request {req_id} returned an error "
                f"(retCode={message.get('retCode')}, "
                f"retMsg={message.get('retMsg')!r}). Raw response: {message}"
            )
            if error_callback is None:
                return
            self._invoke_user_callback(error_callback, message, req_id)
            return

        if callback is None:
            # Unknown or missing reqId: no registered callback to invoke.
            # Log at warning so operators can spot stray frames without
            # tearing down the WS read thread on a KeyError.
            logger.warning(
                f"WebSocket response for unregistered reqId {req_id!r}; "
                f"dropping. Raw response: {message}"
            )
            return

        self._invoke_user_callback(callback, message, req_id)

    @staticmethod
    def _invoke_user_callback(func, message, req_id):
        try:
            func(message)
        except Exception:
            logger.exception(
                f"User callback for WebSocket request {req_id} raised an "
                f"exception; suppressing to keep the WS read thread alive."
            )

    def _set_callback(self, topic, callback_function, error_callback=None):
        self.callback_directory[topic] = (callback_function, error_callback)

    def _pop_callback(self, topic):
        return self.callback_directory.pop(topic, (None, None))

    def _send_order_operation(
        self, operation, callback, request, error_callback=None
    ):
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
        self._set_callback(request_id, callback, error_callback)
