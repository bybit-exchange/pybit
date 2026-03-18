from ._http_manager import _V5HTTPManager
from .broker import Broker


class BrokerHTTP(_V5HTTPManager):
    def get_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/earning
        """
        self.logger.warning(
            "get_broker_earnings() is deprecated. See get_exchange_broker_earnings().")

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )

    def get_exchange_broker_earnings(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-earning
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_EXCHANGE_BROKER_EARNINGS}",
            query=kwargs,
            auth=True,
        )

    def get_exchange_broker_account_info(self) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/account-info
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_EXCHANGE_BROKER_ACCOUNT_INFO}",
            auth=True,
        )

    def get_subaccount_deposit_records(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/sub-deposit-record
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_SUBACCOUNT_DEPOSIT_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_voucher_spec(self, **kwargs) -> dict:
        """
        Required args:
            id (string): Voucher ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/reward/voucher
        """

        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Broker.GET_VOUCHER_SPEC}",
            query=kwargs,
            auth=True,
        )

    def issue_voucher(self, **kwargs) -> dict:
        """
        Required args:
            accountId (string): User ID
            awardId (string): Voucher ID
            specCode (string): Customised unique spec code, up to 8 characters ID
            amount (string): Issue amount
            brokerId (string): Broker ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/reward/issue-voucher
        """

        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Broker.ISSUE_VOUCHER}",
            query=kwargs,
            auth=True,
        )

    def get_issued_voucher(self, **kwargs) -> dict:
        """
        Required args:
            accountId (string): User ID
            awardId (string): Voucher ID
            specCode (string): Customised unique spec code, up to 8 characters ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/reward/get-issue-voucher
        """

        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Broker.GET_ISSUED_VOUCHER}",
            query=kwargs,
            auth=True,
        )

    def get_broker_all_rate_limits(self, **kwargs) -> dict:
        """
        Required args:
            limit (string): Limit for data size per page.
            cursor (string): Cursor.
            uids (string): Multiple UIDs across different master accounts, separated by commas. Returns all subaccounts by default

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/query-all
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_ALL_RATE_LIMITS}",
            query=kwargs,
            auth=True,
        )

    def get_broker_rate_limit_cap(self, **kwargs) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/query-cap
        """

        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Broker.GET_BROKER_RATE_LIMIT_CAP}",
            query=kwargs,
            auth=True,
        )

    def set_broker_rate_limit(self, **kwargs) -> dict:
        """
        Required args:
            list (array): List of data
                uids (string): Multiple UIDs separated by commas, e.g., "uid1,uid2,uid3"
                bizType (string): Business type
                rate (integer): API rate limit per second

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/set
        """

        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Broker.SET_BROKER_RATE_LIMIT}",
            query=kwargs,
            auth=True,
        )
