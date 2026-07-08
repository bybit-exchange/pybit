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

    def get_yield(self, **kwargs):
        """Get the yield information for earn products.

        Required args:
            category (string): FlexibleSaving

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/yield
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_YIELD}",
            query=kwargs,
            auth=True,
        )

    def get_hourly_yield(self, **kwargs):
        """Get hourly yield information for earn products.

        Required args:
            category (string): FlexibleSaving

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/hourly-yield
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_HOURLY_YIELD}",
            query=kwargs,
            auth=True,
        )

    def add_liquidity(self, **kwargs):
        """Add liquidity to a Liquidity Mining pool.

        Required args:
            productId (string): Product ID
            orderLinkId (string): User-customised order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/add-liquidity
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.ADD_LIQUIDITY}",
            query=kwargs,
            auth=True,
        )

    def add_margin(self, **kwargs):
        """Add margin to a Liquidity Mining position.

        Required args:
            productId (string): Product ID
            orderLinkId (string): User-customised order ID
            positionId (string): Position ID
            amount (string): Margin amount
            quoteAccountType (string): Quote account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/add-margin
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.ADD_MARGIN}",
            query=kwargs,
            auth=True,
        )

    def claim_liquidity_interest(self, **kwargs):
        """Claim accrued interest from a Liquidity Mining position.

        Required args:
            productId (string): Product ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/claim-interest
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.CLAIM_LIQUIDITY_INTEREST}",
            query=kwargs,
            auth=True,
        )

    def get_advance_earn_order(self, **kwargs):
        """Query advance earn order history.

        Required args:
            category (string): Product category

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_ADVANCE_EARN_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_advance_earn_position(self, **kwargs):
        """Query advance earn positions.

        Required args:
            category (string): Product category

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_ADVANCE_EARN_POSITION}",
            query=kwargs,
            auth=True,
        )

    def get_advance_earn_product(self, **kwargs):
        """Query available advance earn products by category.

        Required args:
            category (string): Product category

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_ADVANCE_EARN_PRODUCT}",
            query=kwargs,
        )

    def get_advance_earn_product_extra_info(self, **kwargs):
        """Query extra info for an advance earn product.

        Required args:
            category (string): Product category

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/product-extra-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_ADVANCE_EARN_PRODUCT_EXTRA_INFO}",
            query=kwargs,
        )

    def get_double_win_leverage(self, **kwargs):
        """Get double-win leverage calculation for a product.

        Required args:
            productId (integer): Product ID
            initialPrice (string): Initial price
            lowerPrice (string): Lower price bound
            upperPrice (string): Upper price bound

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/double-win-leverage
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_DOUBLE_WIN_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    def get_earn_apr_history(self, **kwargs):
        """Get historical APR values for an earn product.

        Required args:
            category (string): Product category
            productId (string): Product ID
            startTime (integer): Start timestamp (ms)
            endTime (integer): End timestamp (ms)

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/apr-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_EARN_APR_HISTORY}",
            query=kwargs,
        )

    def get_fixed_term_order(self, **kwargs):
        """Query fixed term earn order history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_FIXED_TERM_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_fixed_term_position(self, **kwargs):
        """Query fixed term earn positions.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_FIXED_TERM_POSITION}",
            query=kwargs,
            auth=True,
        )

    def get_fixed_term_product(self, **kwargs):
        """Query available fixed term earn products.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_FIXED_TERM_PRODUCT}",
            query=kwargs,
        )

    def get_hold_to_earn_product(self, **kwargs):
        """Get the list of Hold-to-Earn products.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/hold-to-earn/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_HOLD_TO_EARN_PRODUCT}",
            query=kwargs,
        )

    def get_hold_to_earn_yield_history(self, **kwargs):
        """Get yield history for Hold-to-Earn products.

        Required args:
            limit (integer): Number of records per page

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/hold-to-earn/yield-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_HOLD_TO_EARN_YIELD_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_liquidity_mining_liquidation_records(self, **kwargs):
        """Get Liquidity Mining liquidation records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/liquidation-records
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_LIQUIDITY_MINING_LIQUIDATION_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_liquidity_mining_orders(self, **kwargs):
        """Get Liquidity Mining order history.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_LIQUIDITY_MINING_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_liquidity_mining_positions(self, **kwargs):
        """Get active Liquidity Mining positions.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_LIQUIDITY_MINING_POSITIONS}",
            query=kwargs,
            auth=True,
        )

    def get_liquidity_mining_products(self, **kwargs):
        """Get the list of Liquidity Mining products.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_LIQUIDITY_MINING_PRODUCTS}",
            query=kwargs,
        )

    def get_liquidity_mining_yield_records(self, **kwargs):
        """Get Liquidity Mining yield claim records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/yield-records
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_LIQUIDITY_MINING_YIELD_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_rwa_nav_chart(self, **kwargs):
        """Get the NAV (Net Asset Value) chart for an RWA product.

        Required args:
            productId (integer): Product ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/rwa/nav-chart
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_RWA_NAV_CHART}",
            query=kwargs,
        )

    def get_rwa_order_list(self, **kwargs):
        """Get the RWA earn order history for the account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/rwa/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_RWA_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_rwa_position_list(self, **kwargs):
        """Get the list of RWA earn positions for the account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/rwa/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_RWA_POSITION_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_rwa_product_list(self, **kwargs):
        """Get the list of available RWA (Real World Asset) earn products.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/rwa/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_RWA_PRODUCT_LIST}",
            query=kwargs,
        )

    def get_smart_leverage_redeem_est_amount_list(self, **kwargs):
        """Get estimated redeem amounts for smart leverage positions.

        Required args:
            category (string): Product category
            positionIds (array): List of position IDs

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/get-redeem-est-amount-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_SMART_LEVERAGE_REDEEM_EST_AMOUNT_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_token_daily_yield(self, **kwargs):
        """Query daily yield for a token earn position.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/yield
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_DAILY_YIELD}",
            query=kwargs,
            auth=True,
        )

    def get_token_historical_apr(self, **kwargs):
        """Query historical APR for a token.

        Required args:
            coin (string): Coin
            range (integer): Time range

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/history-apr
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_HISTORICAL_APR}",
            query=kwargs,
        )

    def get_token_hourly_yield(self, **kwargs):
        """Query hourly yield for a token earn position.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/hourly-yield
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_HOURLY_YIELD}",
            query=kwargs,
            auth=True,
        )

    def get_token_order_list(self, **kwargs):
        """Query token order history.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_token_position(self, **kwargs):
        """Query token earn position for a coin.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/position
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_POSITION}",
            query=kwargs,
            auth=True,
        )

    def get_token_product(self, **kwargs):
        """Query token product info by coin.

        Required args:
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.GET_TOKEN_PRODUCT}",
            query=kwargs,
        )

    def list_earn_coupons(self, **kwargs):
        """List earn coupons available to the account.

        Required args:
            category (string): Product category

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/coupons
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.LIST_EARN_COUPONS}",
            query=kwargs,
            auth=True,
        )

    def modify_earn_position(self, **kwargs):
        """Modify an earn position (e.g. toggle auto-reinvest).

        Required args:
            category (string): Product category
            productId (integer): Product ID
            positionId (integer): Position ID
            autoReinvest (integer): Auto-reinvest flag (0 / 1)

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/position/modify
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.MODIFY_EARN_POSITION}",
            query=kwargs,
            auth=True,
        )

    def place_advance_earn_order(self, **kwargs):
        """Place an advance earn order (stake/redeem/etc.).

        Required args:
            category (string): Product category
            productId (integer): Product ID
            orderType (string): Order type
            amount (string): Order amount
            accountType (string): Account type
            coin (string): Coin
            orderLinkId (string): User-defined order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/advance/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PLACE_ADVANCE_EARN_ORDER}",
            query=kwargs,
            auth=True,
        )

    def place_fixed_term_order(self, **kwargs):
        """Place a fixed term earn order.

        Required args:
            productId (string): Product ID
            category (string): Product category
            coin (string): Coin
            amount (string): Order amount
            accountType (string): Account type
            orderLinkId (string): User-defined order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PLACE_FIXED_TERM_ORDER}",
            query=kwargs,
            auth=True,
        )

    def place_rwa_order(self, **kwargs):
        """Place a stake or redeem order for an RWA earn product.

        Required args:
            productId (integer): Product ID
            orderType (string): Order type (Stake / Redeem)
            coin (string): Coin name
            orderLinkId (string): User-customised order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/rwa/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PLACE_RWA_ORDER}",
            query=kwargs,
            auth=True,
        )

    def place_token_order(self, **kwargs):
        """Place a token mint/redeem order.

        Required args:
            coin (string): Coin
            orderLinkId (string): User-defined order ID
            orderType (string): Order type (mint/redeem)
            amount (string): Order amount
            accountType (string): Account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/token/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PLACE_TOKEN_ORDER}",
            query=kwargs,
            auth=True,
        )

    def pwm_asset_trend(self, **kwargs):
        """Get plan asset trend.

        Required args:
            planId (string): Investment plan ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/asset-trend
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_ASSET_TREND}",
            query=kwargs,
            auth=True,
        )

    def pwm_claim(self, **kwargs):
        """Claim available funds from an investment plan.

        Required args:
            planId (string): Investment plan ID
            orderLinkId (string): Client-generated unique order link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/claim
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_CLAIM}",
            query=kwargs,
            auth=True,
        )

    def pwm_create_custom_plan(self, **kwargs):
        """Create a PWM custom investment plan (direct mode).

        Required args:
            products (array): List of product entries composing the custom plan.
            orderLinkId (string): Client-supplied unique order link ID.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/customize-plan/create
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_CREATE_CUSTOM_PLAN}",
            query=kwargs,
            auth=True,
        )

    def pwm_fund_nav(self, **kwargs):
        """Get fund historical NAV.

        Required args:
            fundId (string): Fund ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/fund-nav
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_FUND_NAV}",
            query=kwargs,
            auth=True,
        )

    def pwm_fund_transfer(self, **kwargs):
        """Transfer funds between custody sub-accounts.

        Required args:
            transferId (string): Client-generated unique transfer ID
            fromUserId (integer): From user UID
            toUserId (integer): To user UID
            amount (string): Transfer amount
            coin (string): Coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/fund-transfer
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_FUND_TRANSFER}",
            query=kwargs,
            auth=True,
        )

    def pwm_get_new_plan_detail(self, **kwargs):
        """Get pending-subscription plan detail.

        Required args:
            planId (string): Investment plan ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/new-plan
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_GET_NEW_PLAN_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def pwm_get_plan_detail(self, **kwargs):
        """Get plan detail for active or closed investment plans.

        Required args:
            planId (string): Investment plan ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/detail
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_GET_PLAN_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_create_fund(self, **kwargs):
        """Create a pending-subscription fund.

        Required args:
            fundName (string): Fund name
            coin (string): Coin
            profitShareRate (string): Profit share rate
            managementFeeRate (string): Management fee rate
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/create-fund
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_CREATE_FUND}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_create_investment_plan(self, **kwargs):
        """Create an investment plan for a client.

        Required args:
            accountUid (string): Client account UID
            planName (string): Investment plan name
            planType (string): Plan type
            investmentDistribution (array): Investment distribution across funds
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/create-investment-plan
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_CREATE_INVESTMENT_PLAN}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_create_sub_account(self, **kwargs):
        """Create a fund sub-account.

        Required args:
            fundId (string): Fund ID
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/create-sub-account
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_CREATE_SUB_ACCOUNT}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_get_investment_plans(self, **kwargs):
        """Query institution's investment plans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/get-investment-plan
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_INST_GET_INVESTMENT_PLANS}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_list_funds(self, **kwargs):
        """Query institution's managed funds.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/all-funds
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_INST_LIST_FUNDS}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_list_orders(self, **kwargs):
        """Query fund subscription and redemption orders.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/all-order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_INST_LIST_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_manage_investment_plan(self, **kwargs):
        """Update investment plan status and funds.

        Required args:
            planId (string): Investment plan ID
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/manage-investment-plan
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_MANAGE_INVESTMENT_PLAN}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_manage_order(self, **kwargs):
        """Approve or reject a fund order.

        Required args:
            orderId (string): Order ID
            action (string): Action to perform (approve or reject)
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/manage-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_MANAGE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def pwm_inst_settle_profit(self, **kwargs):
        """Execute profit settlement for a managed fund.

        Required args:
            fundId (string): Fund ID
            reqLinkId (string): Client-generated unique request link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/asset-manager/settle-profit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INST_SETTLE_PROFIT}",
            query=kwargs,
            auth=True,
        )

    def pwm_invest_more(self, **kwargs):
        """Invest more into an active investment plan.

        Required args:
            planId (string): Investment plan ID
            category (string): Product category
            productId (string): Product ID
            amount (string): Investment amount
            orderLinkId (string): Client-generated unique order link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/invest-more
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_INVEST_MORE}",
            query=kwargs,
            auth=True,
        )

    def pwm_list_investment_plans(self, **kwargs):
        """List investment plans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/all
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_LIST_INVESTMENT_PLANS}",
            query=kwargs,
            auth=True,
        )

    def pwm_list_order(self, **kwargs):
        """List PWM investment plan orders.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/order
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_LIST_ORDER}",
            query=kwargs,
            auth=True,
        )

    def pwm_list_product_cards(self, **kwargs):
        """List available PWM product cards for direct-mode custom plans.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/customize-plan/product
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_LIST_PRODUCT_CARDS}",
            query=kwargs,
        )

    def pwm_query_fund_transfer_result(self, **kwargs):
        """Query fund transfer records.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/query-fund-transfer-result
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Earn.PWM_QUERY_FUND_TRANSFER_RESULT}",
            query=kwargs,
            auth=True,
        )

    def pwm_redeem(self, **kwargs):
        """Redeem from an investment plan.

        Required args:
            planId (string): Investment plan ID
            category (string): Product category
            productId (string): Product ID
            orderLinkId (string): Client-generated unique order link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/redeem
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_REDEEM}",
            query=kwargs,
            auth=True,
        )

    def pwm_subscribe(self, **kwargs):
        """One-click subscribe to a pending investment plan.

        Required args:
            planId (string): Investment plan ID
            orderLinkId (string): Client-generated unique order link ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/pwm/investment-plan/subscribe
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.PWM_SUBSCRIBE}",
            query=kwargs,
            auth=True,
        )

    def redeem_fixed_term(self, **kwargs):
        """Redeem a fixed term earn position.

        Required args:
            productId (string): Product ID
            category (string): Product category
            positionId (string): Position ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/redeem
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.REDEEM_FIXED_TERM}",
            query=kwargs,
            auth=True,
        )

    def reinvest_liquidity(self, **kwargs):
        """Reinvest interest from a Liquidity Mining position.

        Required args:
            productId (string): Product ID
            orderLinkId (string): User-customised order ID
            positionId (string): Position ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/reinvest
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.REINVEST_LIQUIDITY}",
            query=kwargs,
            auth=True,
        )

    def remove_liquidity(self, **kwargs):
        """Remove liquidity from a Liquidity Mining position.

        Required args:
            productId (string): Product ID
            orderLinkId (string): User-customised order ID
            positionId (string): Position ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/liquidity-mining/remove-liquidity
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.REMOVE_LIQUIDITY}",
            query=kwargs,
            auth=True,
        )

    def set_fixed_term_auto_invest(self, **kwargs):
        """Enable or disable auto-invest for a fixed term position.

        Required args:
            productId (string): Product ID
            category (string): Product category
            positionId (string): Position ID
            status (string): Auto-invest status

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/earn/fixed-term/position/auto-invest
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Earn.SET_FIXED_TERM_AUTO_INVEST}",
            query=kwargs,
            auth=True,
        )
