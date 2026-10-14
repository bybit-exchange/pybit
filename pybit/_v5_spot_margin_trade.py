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

    def get_tiered_collateral_ratio(self, **kwargs):
        """UTA loan tiered collateral ratio

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/tier-collateral-ratio
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_TIERED_COLLATERAL_RATIO}",
            query=kwargs,
        )

    def get_auto_repay_mode(self, **kwargs):
        """Get spot automatic repayment mode

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/get-auto-repay-mode
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_AUTO_REPAY_MODE}",
            query=kwargs,
            auth=True,
        )

    def set_auto_repay_mode(self, **kwargs):
        """Set spot automatic repayment mode

        Required args:
            autoRepayMode (string): 1: On;  0: Off.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-auto-repay-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.SET_AUTO_REPAY_MODE}",
            query=kwargs,
            auth=True,
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

    def spot_margin_trade_get_max_borrowable(self, **kwargs):
        """UTA only. Get the maximum borrowable amount for spot margin.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/max-borrowable
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_MAX_BORROWABLE}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_get_position_tiers(self, **kwargs):
        """Get spot margin position tiers information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/position-tiers
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_POSITION_TIERS}",
            query=kwargs,
        )

    def spot_margin_trade_get_coin_state(self, **kwargs):
        """Get spot margin coin state information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/coinstate
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_COIN_STATE}",
            query=kwargs,
        )

    def spot_margin_trade_get_repayment_available_amount(self, **kwargs):
        """UTA only. Get repayment available amount.

        Required args:
            coin (string): Coin name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/repayment-available-amount
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_REPAYMENT_AVAILABLE_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_get_currency_data(self, **kwargs):
        """Get spot margin currency data information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/currency-data
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_CURRENCY_DATA}",
            query=kwargs,
        )

    def query_fixed_available_inventory(self, **kwargs):
        """Query Fixed-Rate Available Inventory

        Required args:
            currency (string): Borrow coin name, uppercase only. e.g. `USDT`, `BTC`. **Required.**
            term (string): Loan term in days. e.g. `7`, `14`, `30`, `90`, `180`. **Required.**
            annualRate (string): Annual interest rate. e.g. `0.02` means 2%. **Required.**
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixed-available-inventory
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.QUERY_FIXED_AVAILABLE_INVENTORY}",
            query=kwargs,
            auth=True,
        )

    def account_fixed_borrow(self, **kwargs):
        """Fixed-Rate Borrow

        Required args:
            orderCurrency (string): Borrow coin name, uppercase only. e.g. `USDT`, `BTC`.
            orderAmount (string): Borrow amount.
            annualRate (string): Annual interest rate. e.g. `0.02` means 2%.
            term (string): Loan term in days. Supported values: `7`, `14`, `30`, `90`, `180`.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixedborrow
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.ACCOUNT_FIXED_BORROW}",
            query=kwargs,
            auth=True,
        )

    def query_fixed_borrow_contracts(self, **kwargs):
        """Query Fixed-Rate Borrow Contracts
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixedborrow-contract-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.QUERY_FIXED_BORROW_CONTRACTS}",
            query=kwargs,
            auth=True,
        )

    def query_fixed_borrow_orders(self, **kwargs):
        """Query Fixed-Rate Borrow Orders
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixedborrow-order-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.QUERY_FIXED_BORROW_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def query_fixed_borrow_market(self, **kwargs):
        """Query Fixed-Rate Borrow Market

        Required args:
            orderCurrency (string): Borrow coin name, uppercase only. e.g. `USDT`, `BTC`. **Required.**

        Optional args:
            term (string): Fixed term in days.
            orderBy (string): Sort field: `apy`, `term`, or `quantity`.
            sort (integer): Sort direction. `0`: ascending, `1`: descending.
            limit (integer): Number of records per page, from 1 to 100.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixedborrow-order-quote
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.QUERY_FIXED_BORROW_MARKET}",
            query=kwargs,
            auth=True,
        )

    def renew_fixed_borrow(self, **kwargs):
        """Renew Fixed-Rate Borrow

        Required args:
            loanId (string): The loan contract ID (corresponds to match order ID). Required.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/fixedborrow-renew
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.RENEW_FIXED_BORROW}",
            query=kwargs,
            auth=True,
        )

    def get_spot_margin_trade_flexible_available_inventory(self, **kwargs):
        """Get Flexible Available Inventory

        Required args:
            currency (string): Coin name, uppercase only. e.g. `BTC`
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/flexible-available-inventory
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.GET_SPOT_MARGIN_TRADE_FLEXIBLE_AVAILABLE_INVENTORY}",
            query=kwargs,
            auth=True,
        )

    def query_borrow_liability(self, **kwargs):
        """Query Borrow Liability

        Required args:
            currency (string): Coin name, uppercase only. e.g. `USDT`, `BTC`. **Required.**
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/spot-margin-uta/liability
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.QUERY_BORROW_LIABILITY}",
            query=kwargs,
            auth=True,
        )
