from ._http_manager import _V5HTTPManager
from .asset import Asset


class AssetHTTP(_V5HTTPManager):
    def get_coin_exchange_records(self, **kwargs):
        """Query the coin exchange records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/exchange
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_COIN_EXCHANGE_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_option_delivery_record(self, **kwargs):
        """Query option delivery records, sorted by deliveryTime in descending order

        Required args:
            category (string): Product type. option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/option-delivery
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_OPTION_DELIVERY_RECORD}",
            query=kwargs,
            auth=True,
        )

    def get_usdc_contract_settlement(self, **kwargs):
        """Query session settlement records of USDC perpetual and futures

        Required args:
            category (string): Product type. linear

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/settlement
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_USDC_CONTRACT_SETTLEMENT}",
            query=kwargs,
            auth=True,
        )

    def get_spot_asset_info(self, **kwargs):
        """Query asset information

        Required args:
            accountType (string): Account type. SPOT

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/asset-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_SPOT_ASSET_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_coins_balance(self, **kwargs):
        """You could get all coin balance of all account types under the master account, and sub account.

        Required args:
            memberId (string): User Id. It is required when you use master api key to check sub account coin balance
            accountType (string): Account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/all-balance
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_ALL_COINS_BALANCE}",
            query=kwargs,
            auth=True,
        )

    def get_coin_balance(self, **kwargs):
        """Query the balance of a specific coin in a specific account type. Supports querying sub UID's balance.

        Required args:
            memberId (string): UID. Required when querying sub UID balance
            accountType (string): Account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/account-coin-balance
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_SINGLE_COIN_BALANCE}",
            query=kwargs,
            auth=True,
        )

    def get_transferable_coin(self, **kwargs):
        """Query the transferable coin list between each account type

        Required args:
            fromAccountType (string): From account type
            toAccountType (string): To account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/transferable-coin
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_TRANSFERABLE_COIN}",
            query=kwargs,
            auth=True,
        )

    def create_internal_transfer(self, **kwargs):
        """Create the internal transfer between different account types under the same UID.

        Required args:
            transferId (string): UUID. Please manually generate a UUID
            coin (string): Coin
            amount (string): Amount
            fromAccountType (string): From account type
            toAccountType (string): To account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/create-inter-transfer
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.CREATE_INTERNAL_TRANSFER}",
            query=kwargs,
            auth=True,
        )

    def get_internal_transfer_records(self, **kwargs):
        """Query the internal transfer records between different account types under the same UID.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/inter-transfer-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_INTERNAL_TRANSFER_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_sub_uid(self, **kwargs):
        """Query the sub UIDs under a main UID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/sub-uid-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_SUB_UID}",
            query=kwargs,
            auth=True,
        )

    def enable_universal_transfer_for_sub_uid(self, **kwargs):
        """Transfer between sub-sub or main-sub

        Required args:
            subMemberIds (array): This list has a single item. Separate multiple UIDs by comma, e.g., "uid1,uid2,uid3"

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/enable-unitransfer-subuid
        """
        self.logger.warning("enable_universal_transfer_for_sub_uid() is depreciated. You no longer need to configure transferable sub UIDs. Now, all sub UIDs are automatically enabled for universal transfer.")
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.ENABLE_UT_FOR_SUB_UID}",
            query=kwargs,
            auth=True,
        )

    def create_universal_transfer(self, **kwargs):
        """Transfer between sub-sub or main-sub. Please make sure you have enabled universal transfer on your sub UID in advance.

        Required args:
            transferId (string): UUID. Please manually generate a UUID
            coin (string): Coin
            amount (string): Amount
            fromMemberId (integer): From UID
            toMemberId (integer): To UID
            fromAccountType (string): From account type
            toAccountType (string): To account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/unitransfer
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.CREATE_UNIVERSAL_TRANSFER}",
            query=kwargs,
            auth=True,
        )

    def get_universal_transfer_records(self, **kwargs):
        """Query universal transfer records

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/unitransfer-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_UNIVERSAL_TRANSFER_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_allowed_deposit_coin_info(self, **kwargs):
        """Query allowed deposit coin information. To find out paired chain of coin, please refer coin info api.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/deposit-coin-spec
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_ALLOWED_DEPOSIT_COIN_INFO}",
            query=kwargs,
            auth=True,
        )

    def set_deposit_account(self, **kwargs):
        """Set auto transfer account after deposit. The same function as the setting for Deposit on web GUI

        Required args:
            accountType (string): Account type: UNIFIED,SPOT,OPTION,CONTRACT,FUND

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/set-deposit-acct
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.SET_DEPOSIT_ACCOUNT}",
            query=kwargs,
            auth=True,
        )

    def get_deposit_records(self, **kwargs):
        """Query deposit records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/deposit-record
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_DEPOSIT_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_sub_deposit_records(self, **kwargs):
        """Query subaccount's deposit records by MAIN UID's API key.

        Required args:
            subMemberId (string): Sub UID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/sub-deposit-record
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_SUB_ACCOUNT_DEPOSIT_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_internal_deposit_records(self, **kwargs):
        """Query deposit records within the Bybit platform. These transactions are not on the blockchain.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/internal-deposit-record
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_INTERNAL_DEPOSIT_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_master_deposit_address(self, **kwargs):
        """Query the deposit address information of MASTER account.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/master-deposit-addr
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_MASTER_DEPOSIT_ADDRESS}",
            query=kwargs,
            auth=True,
        )

    def get_sub_deposit_address(self, **kwargs):
        """Query the deposit address information of SUB account.

        Required args:
            coin (string): Coin
            chainType (string): Chain, e.g.,ETH

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/sub-deposit-addr
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_SUB_DEPOSIT_ADDRESS}",
            query=kwargs,
            auth=True,
        )

    def get_coin_info(self, **kwargs):
        """Query coin information, including chain information, withdraw and deposit status.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/coin-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_COIN_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_withdrawal_records(self, **kwargs):
        """Query withdrawal records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/withdraw-record
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_WITHDRAWAL_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_withdrawable_amount(self, **kwargs):
        """Get withdrawable amount

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/delay-amount
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_WITHDRAWABLE_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def withdraw(self, **kwargs):
        """Withdraw assets from your Bybit account. You can make an off-chain transfer if the target wallet address is from Bybit. This means that no blockchain fee will be charged.

        Required args:
            coin (string): Coin
            chain (string): Chain
            address (string): Wallet address
            tag (string): Tag. Required if tag exists in the wallet address list
            amount (string): Withdraw amount
            timestamp (integer): Current timestamp (ms). Used for preventing from withdraw replay

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/withdraw
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.WITHDRAW}",
            query=kwargs,
            auth=True,
        )

    def cancel_withdrawal(self, **kwargs):
        """Cancel the withdrawal

        Required args:
            id (string): Withdrawal ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/cancel-withdraw
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.CANCEL_WITHDRAWAL}",
            query=kwargs,
            auth=True,
        )

    def get_convert_coin_list(self, **kwargs):
        """Query for the list of coins you can convert to/from.

        Required args:
            accountType (string): Wallet type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/convert/convert-coin-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_CONVERT_COIN_LIST}",
            query=kwargs,
            auth=True,
        )

    def request_a_quote(self, **kwargs):
        """
        Required args:
            fromCoin (string): Convert from coin (coin to sell)
            toCoin (string): Convert to coin (coin to buy)
            requestCoin (string): Request coin, same as fromCoin
            requestAmount (string): request coin amount (the amount you want to sell)

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.REQUEST_A_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def confirm_a_quote(self, **kwargs):
        """
        Required args:
            quoteTxId (string): The quoteTxId from request_a_quote

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/convert/confirm-quote
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Asset.CONFIRM_A_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def get_convert_status(self, **kwargs):
        """
        Required args:
            quoteTxId (string): Quote tx ID
            accountType (string): Wallet type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_CONVERT_STATUS}",
            query=kwargs,
            auth=True,
        )

    def get_convert_history(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Asset.GET_CONVERT_HISTORY}",
            query=kwargs,
            auth=True,
        )
