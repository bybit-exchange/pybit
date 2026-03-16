from pybit.asyncio.client import AsyncClient
from pybit.spot_margin_trade import SpotMarginTrade


class AsyncSpotMarginTradeHTTP(AsyncClient):
    async def spot_margin_trade_get_vip_margin_data(self, **kwargs) -> dict:
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

    async def spot_margin_trade_toggle_margin_trade(self, **kwargs) -> dict:
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

    async def spot_margin_trade_set_leverage(self, **kwargs) -> dict:
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

    async def spot_margin_trade_get_historical_interest_rate(self, **kwargs) -> dict:
        """UTA only. Queries up to six months of borrowing interest rates.

        Required args:
            currency (string): Coin name, uppercase only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/historical-interest
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.HISTORICAL_INTEREST}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_get_vip_margin_data(self, **kwargs) -> dict:
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

    async def get_tiered_collateral_ratio(self, **kwargs) -> dict:
        """UTA loan tiered collateral ratio

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/tier-collateral-ratio
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_TIERED_COLLATERAL_RATIO}",
            query=kwargs,
        )

    async def get_auto_repay_mode(self, **kwargs) -> dict:
        """Get spot automatic repayment mode

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/get-auto-repay-mode
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_AUTO_REPAY_MODE}",
            query=kwargs,
            auth=True,
        )

    async def set_auto_repay_mode(self, **kwargs) -> dict:
        """Set spot automatic repayment mode

        Required args:
            autoRepayMode (string): 1: On;  0: Off.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-auto-repay-mode
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.SET_AUTO_REPAY_MODE}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_normal_get_margin_coin_info(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_get_borrowable_coin_info(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_get_interest_quota(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_get_loan_account_info(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_borrow(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_repay(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_get_borrow_order_detail(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_get_repayment_order_detail(self, **kwargs) -> dict:
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

    async def spot_margin_trade_normal_toggle_margin_trade(self, **kwargs) -> dict:
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

    async def spot_margin_trade_get_max_borrowable(self, **kwargs) -> dict:
        """UTA only. Get the maximum borrowable amount for spot margin.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/max-borrowable
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_MAX_BORROWABLE}",
            query=kwargs,
            auth=True,
        )

    async def spot_margin_trade_get_position_tiers(self, **kwargs) -> dict:
        """Get spot margin position tiers information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/position-tiers
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_POSITION_TIERS}",
            query=kwargs,
        )

    async def spot_margin_trade_get_coin_state(self, **kwargs) -> dict:
        """Get spot margin coin state information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/coinstate
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_COIN_STATE}",
            query=kwargs,
        )

    async def spot_margin_trade_get_repayment_available_amount(self, **kwargs) -> dict:
        """UTA only. Get repayment available amount.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/repayment-available-amount
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_REPAYMENT_AVAILABLE_AMOUNT}",
            query=kwargs,
            auth=True,
        )
