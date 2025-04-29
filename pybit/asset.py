from enum import Enum


class Asset(str, Enum):
    GET_COIN_EXCHANGE_RECORDS = "/v5/asset/exchange/order-record"
    GET_OPTION_DELIVERY_RECORD = "/v5/asset/delivery-record"
    GET_USDC_CONTRACT_SETTLEMENT = "/v5/asset/settlement-record"
    GET_SPOT_ASSET_INFO = "/v5/asset/transfer/query-asset-info"
    GET_ALL_COINS_BALANCE = "/v5/asset/transfer/query-account-coins-balance"
    GET_SINGLE_COIN_BALANCE = "/v5/asset/transfer/query-account-coin-balance"
    GET_TRANSFERABLE_COIN = "/v5/asset/transfer/query-transfer-coin-list"
    CREATE_INTERNAL_TRANSFER = "/v5/asset/transfer/inter-transfer"
    GET_INTERNAL_TRANSFER_RECORDS = (
        "/v5/asset/transfer/query-inter-transfer-list"
    )
    GET_SUB_UID = "/v5/asset/transfer/query-sub-member-list"
    ENABLE_UT_FOR_SUB_UID = "/v5/asset/transfer/save-transfer-sub-member"
    CREATE_UNIVERSAL_TRANSFER = "/v5/asset/transfer/universal-transfer"
    GET_UNIVERSAL_TRANSFER_RECORDS = (
        "/v5/asset/transfer/query-universal-transfer-list"
    )
    GET_ALLOWED_DEPOSIT_COIN_INFO = "/v5/asset/deposit/query-allowed-list"
    SET_DEPOSIT_ACCOUNT = "/v5/asset/deposit/deposit-to-account"
    GET_DEPOSIT_RECORDS = "/v5/asset/deposit/query-record"
    GET_SUB_ACCOUNT_DEPOSIT_RECORDS = (
        "/v5/asset/deposit/query-sub-member-record"
    )
    GET_INTERNAL_DEPOSIT_RECORDS = "/v5/asset/deposit/query-internal-record"
    GET_MASTER_DEPOSIT_ADDRESS = "/v5/asset/deposit/query-address"
    GET_SUB_DEPOSIT_ADDRESS = "/v5/asset/deposit/query-sub-member-address"
    GET_COIN_INFO = "/v5/asset/coin/query-info"
    GET_WITHDRAWAL_RECORDS = "/v5/asset/withdraw/query-record"
    GET_WITHDRAWABLE_AMOUNT = "/v5/asset/withdraw/withdrawable-amount"
    WITHDRAW = "/v5/asset/withdraw/create"
    CANCEL_WITHDRAWAL = "/v5/asset/withdraw/cancel"
    # Convert
    GET_CONVERT_COIN_LIST = "/v5/asset/exchange/query-coin-list"
    REQUEST_A_QUOTE = "/v5/asset/exchange/quote-apply"
    CONFIRM_A_QUOTE = "/v5/asset/exchange/convert-execute"
    GET_CONVERT_STATUS = "/v5/asset/exchange/convert-result-query"
    GET_CONVERT_HISTORY = "/v5/asset/exchange/query-convert-history"

    def __str__(self) -> str:
        return self.value
