from enum import Enum


class P2P(str, Enum):
    GET_CURRENT_BALANCE = "/v5/asset/transfer/query-account-coins-balance"
    GET_ACCOUNT_INFORMATION = "/v5/p2p/user/personal/info"
    GET_ADS_LIST = "/v5/p2p/item/personal/list"
    GET_AD_DETAILS = "/v5/p2p/item/info"
    UPDATE_AD = "/v5/p2p/item/update"
    REMOVE_AD = "/v5/p2p/item/cancel"
    GET_ORDERS = "/v5/p2p/order/simplifyList"
    GET_PENDING_ORDERS = "/v5/p2p/order/pending/simplifyList"
    GET_COUNTERPARTY_INFO = "/v5/p2p/user/order/personal/info"
    GET_ORDER_DETAILS = "/v5/p2p/order/info"
    RELEASE_ASSETS = "/v5/p2p/order/finish"
    MARK_AS_PAID = "/v5/p2p/order/pay"
    GET_CHAT_MESSAGES = "/v5/p2p/order/message/listpage"
    UPLOAD_CHAT_FILE = "/v5/p2p/oss/upload_file"
    SEND_CHAT_MESSAGE = "/v5/p2p/order/message/send"
    POST_NEW_AD = "/v5/p2p/item/create"
    GET_ONLINE_ADS = "/v5/p2p/item/online"
    GET_USER_PAYMENT_TYPES = "/v5/p2p/user/payment/list"
    QUERY_CHAT_SESSION_LIST = "/v5/p2p/chat/session/list"
    SEND_MESSAGE = "/v5/p2p/chat/message/send"
    GET_MESSAGE_LIST = "/v5/p2p/chat/message/listpage"

    def __str__(self) -> str:
        return self.value
