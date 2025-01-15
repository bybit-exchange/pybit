from ._async_http_manager import _V5ASYNCHTTPManager
from ..spot_margin_trade import SpotMarginTrade


class SpotMarginTradeASYNCHTTP(_V5ASYNCHTTPManager):
    async def spot_margin_trade_get_vip_margin_data(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.VIP_MARGIN_DATA}",
            query=kwargs,
        )

    async def spot_margin_trade_toggle_margin_trade(self, **kwargs):
        """UTA only. Turn spot margin trade on / off.

        Required args:
            spotMarginMode (string): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.TOGGLE_MARGIN_TRADE}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_set_leverage(self, **kwargs):
        """UTA only. Set the user's maximum leverage in spot cross margin

        Required args:
            leverage (string): Leverage. [2, 5].

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.SET_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_get_status_and_leverage(self):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.STATUS_AND_LEVERAGE}",
            auth=True,
        )

    async def spot_margin_trade_normal_get_vip_margin_data(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/vip-margin
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    async def spot_margin_trade_normal_get_margin_coin_info(self, **kwargs):
        """Normal (non-UTA) account only. Turn on / off spot margin trade

        Required args:
            switch (string): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/margin-data
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    async def spot_margin_trade_normal_get_borrowable_coin_info(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrowable-data
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROWABLE_COIN_INFO}",
            query=kwargs,
        )

    async def spot_margin_trade_normal_get_interest_quota(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/interest-quota
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_INTEREST_QUOTA}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_get_loan_account_info(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/account-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_LOAN_ACCOUNT_INFO}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_borrow(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name
            qty (string): Amount to borrow

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrow
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_BORROW}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_repay(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/repay
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_REPAY}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_get_borrow_order_detail(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrow-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROW_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_get_repayment_order_detail(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/repay-order
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_REPAYMENT_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_toggle_margin_trade(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            switch (integer): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/switch-mode
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_TOGGLE_MARGIN_TRADE}",
            query=kwargs,
            auth=True,
        )
