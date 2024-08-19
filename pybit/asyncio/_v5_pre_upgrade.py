from ._async_http_manager import _V5ASYNCHTTPManager
from ..pre_upgrade import PreUpgrade


class PreUpgradeHTTP(_V5ASYNCHTTPManager):
    async def get_pre_upgrade_order_history(self, **kwargs) -> dict:
        """
        After the account is upgraded to a Unified account, you can get the
        orders which occurred before the upgrade.

        Required args:
            category (string): Product type. linear, inverse, option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/order-list
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_ORDER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    async def get_pre_upgrade_trade_history(self, **kwargs) -> dict:
        """
        Get users' execution records which occurred before you upgraded the
        account to a Unified account, sorted by execTime in descending order

        Required args:
            category (string): Product type. linear, inverse, option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/execution
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_TRADE_HISTORY}",
            query=kwargs,
            auth=True,
        )

    async def get_pre_upgrade_closed_pnl(self, **kwargs) -> dict:
        """
        Query user's closed profit and loss records from before you upgraded the
        account to a Unified account. The results are sorted by createdTime in
        descending order.

        Required args:
            category (string): Product type linear, inverse
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/close-pnl
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_CLOSED_PNL}",
            query=kwargs,
            auth=True,
        )

    async def get_pre_upgrade_transaction_log(self, **kwargs) -> dict:
        """
        Query transaction logs which occurred in the USDC Derivatives wallet
        before the account was upgraded to a Unified account.

        Required args:
            category (string): Product type. linear,option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/transaction-log
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_TRANSACTION_LOG}",
            query=kwargs,
            auth=True,
        )

    async def get_pre_upgrade_option_delivery_record(self, **kwargs) -> dict:
        """
        Query delivery records of Option before you upgraded the account to a
        Unified account, sorted by deliveryTime in descending order
        Required args:
            category (string): Product type. option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/delivery
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_OPTION_DELIVERY_RECORD}",
            query=kwargs,
            auth=True,
        )

    async def get_pre_upgrade_usdc_session_settlement(self, **kwargs) -> dict:
        """
        Required args:
            category (string): Product type. linear

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/pre-upgrade/settlement
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{PreUpgrade.GET_PRE_UPGRADE_USDC_SESSION_SETTLEMENT}",
            query=kwargs,
            auth=True,
        )


