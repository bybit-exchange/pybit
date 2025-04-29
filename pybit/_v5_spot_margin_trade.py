from ._http_manager import _V5HTTPManager
from .spot_margin_trade import SpotMarginTrade


class SpotMarginTradeHTTP(_V5HTTPManager):
    def spot_margin_trade_get_vip_margin_data(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.VIP_MARGIN_DATA}",
            query=kwargs,
        )

    def spot_margin_trade_toggle_margin_trade(self, **kwargs):
        """UTA only. Turn spot margin trade on / off.

        Required args:
            spotMarginMode (string): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.TOGGLE_MARGIN_TRADE}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_set_leverage(self, **kwargs):
        """UTA only. Set the user's maximum leverage in spot cross margin

        Required args:
            leverage (string): Leverage. [2, 5].

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.SET_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_get_status_and_leverage(self):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.STATUS_AND_LEVERAGE}",
            auth=True,
        )

    def spot_margin_trade_get_historical_interest_rate(self, **kwargs):
        """UTA only. Queries up to six months of borrowing interest rates.

        Required args:
            currency (string): Coin name, uppercase only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/historical-interest
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.HISTORICAL_INTEREST}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_get_vip_margin_data(self, **kwargs):
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/vip-margin
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    def spot_margin_trade_normal_get_margin_coin_info(self, **kwargs):
        """Normal (non-UTA) account only. Turn on / off spot margin trade

        Required args:
            switch (string): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/margin-data
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    def spot_margin_trade_normal_get_borrowable_coin_info(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrowable-data
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROWABLE_COIN_INFO}",
            query=kwargs,
        )

    def spot_margin_trade_normal_get_interest_quota(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/interest-quota
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_INTEREST_QUOTA}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_get_loan_account_info(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/account-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_LOAN_ACCOUNT_INFO}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_borrow(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name
            qty (string): Amount to borrow

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrow
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_BORROW}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_repay(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/repay
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_REPAY}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_get_borrow_order_detail(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrow-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROW_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_get_repayment_order_detail(self, **kwargs):
        """Normal (non-UTA) account only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/repay-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_REPAYMENT_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_toggle_margin_trade(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            switch (integer): 1: on, 0: off

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-normal/switch-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_TOGGLE_MARGIN_TRADE}",
            query=kwargs,
            auth=True,
        )
