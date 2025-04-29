from ._http_manager import _V5HTTPManager
from .earn import Earn


class EarnHTTP(_V5HTTPManager):
    def get_earn_product_info(self, **kwargs):
        """
        Required args:
            category (string): FlexibleSaving

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/product-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_EARN_PRODUCT_INFO}",
            query=kwargs,
        )

    def stake_or_redeem(self, **kwargs):
        """
        Required args:
            category (string): FlexibleSaving
            orderType (string): Stake, Redeem
            accountType (string): FUND, UNIFIED

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/create-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.STAKE_OR_REDEEM}",
            query=kwargs,
            auth=True,
        )

    def get_stake_or_redemption_history(self, **kwargs):
        """
        Required args:
            category (string): FlexibleSaving

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/order-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_STAKE_OR_REDEMPTION_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_staked_position(self, **kwargs):
        """
        Required args:
            category (string): FlexibleSaving

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_STAKED_POSITION}",
            query=kwargs,
            auth=True,
        )
