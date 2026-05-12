from enum import Enum


class Broker(str, Enum):
    GET_BROKER_EARNINGS = "/v5/broker/earning-record"
    GET_EXCHANGE_BROKER_EARNINGS = "/v5/broker/earnings-info"
    GET_EXCHANGE_BROKER_ACCOUNT_INFO = "/v5/broker/account-info"
    GET_SUBACCOUNT_DEPOSIT_RECORDS = "/v5/broker/asset/query-sub-member-deposit-record"
    GET_VOUCHER_SPEC = "/v5/broker/award/info"
    ISSUE_VOUCHER = "/v5/broker/award/distribute-award"
    GET_ISSUED_VOUCHER = "/v5/broker/award/distribution-record"
    GET_BROKER_ALL_RATE_LIMITS="/v5/broker/apilimit/query-all"
    GET_BROKER_RATE_LIMIT_CAP="/v5/broker/apilimit/query-cap"
    SET_BROKER_RATE_LIMIT="/v5/broker/apilimit/set"

    def __str__(self) -> str:
        return self.value
