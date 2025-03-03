from dataclasses import dataclass, field
import hmac
import hashlib
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64

from pybit import _helpers


def generate_signature(use_rsa_authentication, secret, param_str):
    def generate_hmac():
        hash = hmac.new(
            bytes(secret, "utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256,
        )
        return hash.hexdigest()

    def generate_rsa():
        hash = SHA256.new(param_str.encode("utf-8"))
        encoded_signature = base64.b64encode(
            PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                hash
            )
        )
        return encoded_signature.decode()

    if not use_rsa_authentication:
        return generate_hmac()
    else:
        return generate_rsa()


@dataclass
class AuthService:
    api_key: str = field(default=None)
    api_secret: str = field(default=None)
    rsa_authentication: str = field(default=False)

    def _auth(self, payload, recv_window, timestamp):
        """
        Prepares authentication signature per Bybit API specifications.
        """

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_str = str(timestamp) + self.api_key + str(recv_window) + payload

        return generate_signature(
            self.rsa_authentication, self.api_secret, param_str
        )

    def _prepare_auth_headers(self, recv_window, req_params) -> dict:
        # Prepare signature.
        timestamp = _helpers.generate_timestamp()
        signature = self._auth(
            payload=req_params,
            recv_window=recv_window,
            timestamp=timestamp,
        )
        return {
            "Content-Type": "application/json",
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": str(timestamp),
            "X-BAPI-RECV-WINDOW": str(recv_window),
        }

    def _change_floating_numbers_for_auth_signature(self, query):
        # Bug fix: change floating whole numbers to integers to prevent
        # auth signature errors.
        if query is not None:
            for i in query.keys():
                if isinstance(query[i], float) and query[i] == int(query[i]):
                    query[i] = int(query[i])
