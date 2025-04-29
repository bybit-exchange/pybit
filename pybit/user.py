from enum import Enum


class User(str, Enum):
    CREATE_SUB_UID = "/v5/user/create-sub-member"
    CREATE_SUB_API_KEY = "/v5/user/create-sub-api"
    GET_SUB_UID_LIST = "/v5/user/query-sub-members"
    FREEZE_SUB_UID = "/v5/user/frozen-sub-member"
    GET_API_KEY_INFORMATION = "/v5/user/query-api"
    MODIFY_MASTER_API_KEY = "/v5/user/update-api"
    MODIFY_SUB_API_KEY = "/v5/user/update-sub-api"
    DELETE_MASTER_API_KEY = "/v5/user/delete-api"
    DELETE_SUB_API_KEY = "/v5/user/delete-sub-api"
    GET_AFFILIATE_USER_INFO = "/v5/user/aff-customer-info"
    GET_UID_WALLET_TYPE = "/v5/user/get-member-type"
    DELETE_SUB_UID = "/v5/user/del-submember"
    GET_ALL_SUB_API_KEYS = "/v5/user/sub-apikeys"

    def __str__(self) -> str:
        return self.value
