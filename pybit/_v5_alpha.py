from ._http_manager import _V5HTTPManager
from .alpha import Alpha


class AlphaHTTP(_V5HTTPManager):
    def get_lp_order_list(self, **kwargs):
        """Get LP order history with status and execution details

        Optional args:
            orderType (integer): Filter by type: 0 all (default), 1 stake, 2 redeem.
            tokenCode (string): Filter by token code.
            orderStatus (array): Statuses: 1 processing, 2 success, 3 failed.
            days (integer): Query the last N days. Default 90; maximum 365.
            limit (integer): Results per page. Default 20; maximum 100.
            pageIndex (integer): One-based page number. Default 1.
            poolAddress (string): Filter by pool contract address.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/order-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_lp_pay_token_list(self, **kwargs):
        """Get list of supported payment tokens

        Optional args:
            chainCode (string): Filter by blockchain identifier.
            tokenAddress (string): Filter by token contract address.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/pay-token-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_PAY_TOKEN_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_lp_pay_token_price(self, **kwargs):
        """Get current prices for payment tokens

        Required args:
            tokenCode (array): Array of token codes to query (e.g., ["CEX_1", "CEX_2"]).

        Optional args:
            chainCode (string): Filter by blockchain identifier.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/pay-token-price
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_PAY_TOKEN_PRICE}",
            query=kwargs,
            auth=True,
        )

    def get_lp_pool_info(self, **kwargs):
        """Get detailed information for a specific LP pool

        Required args:
            poolAddress (string): Pool contract address (from getLPPoolList).
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/pool-info
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_POOL_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_lp_pool_list(self, **kwargs):
        """Get LP pool list with optional filters

        Optional args:
            tokenSymbol (string): Token symbol contained by the pool, e.g. ETH or USDC.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/pool-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_POOL_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_lp_position_list(self, **kwargs):
        """Get user's LP positions with rewards and current value
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/position-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_LP_POSITION_LIST}",
            query=kwargs,
            auth=True,
        )

    def execute_lp_redeem(self, **kwargs):
        """Redeem (withdraw) liquidity from a position

        Required args:
            positionId (integer): Position ID (from getLPPositionList).
            poolAddress (string): Pool contract address.
            dercRatio (string): Reduction ratio (0-1).
- "0.25" = redeem 25%
- "0.5" = redeem 50%
- "1" = close entire position (redeem 100%)

        Optional args:
            receiveTokenCode (string): Token code used to receive the redeemed amount.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/redeem
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_LP_REDEEM}",
            query=kwargs,
            auth=True,
        )

    def execute_lp_stake(self, **kwargs):
        """Stake tokens into an LP pool

        Required args:
            positionId (integer): Position ID. Use `0` to create a new position, or provide an existing position ID to add liquidity.

            poolAddress (string): Pool contract address (from getLPPoolInfo).
            payTokenAmount (string): Payment token amount (positive decimal as string).
            payTokenCode (string): Payment token code (e.g., "CEX_1" for USDT).

        Optional args:
            rangeUpper (string): Range upper limit; mutually exclusive with priceUpper.
            rangeLower (string): Range lower limit; mutually exclusive with priceLower.
            priceUpper (string): Price upper limit; mutually exclusive with rangeUpper.
            priceLower (string): Price lower limit; mutually exclusive with rangeLower.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/lp/stake
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_LP_STAKE}",
            query=kwargs,
            auth=True,
        )

    def execute_prediction_buy(self, **kwargs):
        """Buy prediction outcome tokens with USDC

        Required args:
            tokenId (string): Outcome token ID to buy (from getPredictionEventDetail).
            amount (string): USDC amount to invest (positive decimal as string).
            payTokenCode (string): Payment token code. Phase 1 fixed to "USDC".
            orderType (integer): Order type.
            slippage (string): Maximum acceptable price slippage as decimal (e.g., "0.05" = 5% tolerance).
            eventId (string): Event ID associated with the token.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/buy
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_PREDICTION_BUY}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_engine_status(self, **kwargs):
        """Get prediction market matching engine availability status
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/engine-status
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_ENGINE_STATUS}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_event_detail(self, **kwargs):
        """Get prediction event detail with all markets and outcomes

        Optional args:
            eventId (string): Event ID; use slug when available.
            slug (string): URL-friendly slug; takes priority over eventId.
            hasMoreMarkets (boolean): Include related sub-event markets. Default false.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/event-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_EVENT_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_order_book(self, **kwargs):
        """Get full order book snapshot for prediction tokens

        Required args:
            tokenIds (array): List of outcome token IDs. Maximum 20.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/order-book
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_ORDER_BOOK}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_order_estimate(self, **kwargs):
        """Estimate buy or sell order fill amount and fees before execution

        Required args:
            tokenId (string): Outcome token ID (from getPredictionEventDetail or getPredictionMarketList).
            side (integer): Order side.
            eventId (string): Event ID associated with this token.
            amount (string): For BUY: USDC amount to invest (e.g., "100").
For SELL: number of shares to sell (e.g., "50").

            orderType (integer): Order type.

        Optional args:
            payTokenCode (string): Required for BUY; phase 1 is fixed to USDC.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/order-estimate
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_ORDER_ESTIMATE}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_order_list(self, **kwargs):
        """Get user's prediction market order history

        Optional args:
            status (integer): Filter by prediction order status.
            tokenId (string): Filter by outcome token ID.
            eventId (string): Filter by event ID.
            side (integer): Filter by trade direction.
            days (integer): Look back N days. Maximum 90.
            limit (integer): Number of records per page.
            pageIndex (integer): Page number starting from 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/order-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_pay_token_list(self, **kwargs):
        """Get available payment tokens (USDC) for prediction market
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/pay-token-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_PAY_TOKEN_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_portfolio_summary(self, **kwargs):
        """Get user's prediction market portfolio overview

        Optional args:
            eventType (integer): Filter by prediction event type.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/portfolio-summary
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_PORTFOLIO_SUMMARY}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_position_history(self, **kwargs):
        """Get user's historical closed prediction market positions

        Optional args:
            tokenId (string): Filter by outcome token ID.
            eventId (string): Filter by event ID.
            result (integer): Filter by position outcome.
            days (integer): Look back N days. Maximum 90.
            limit (integer): Number of records per page.
            pageIndex (integer): Page number starting from 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/position-history
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_POSITION_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_position_list(self, **kwargs):
        """Get user's current open prediction market positions

        Optional args:
            tokenId (string): Filter by outcome token ID.
            eventId (string): Filter by event ID.
            limit (integer): Number of records per page.
            pageIndex (integer): Page number starting from 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/position-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_POSITION_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_price_history(self, **kwargs):
        """Get historical price chart data for prediction tokens

        Required args:
            tokenId (string): Outcome token ID.
            interval (string): Time interval. Valid values: `1H`, `6H`, `1D`,
                `1W`, `1M`, `ALL`.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/price-history
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_PRICE_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def execute_prediction_sell(self, **kwargs):
        """Sell prediction outcome token shares for USDC

        Required args:
            tokenId (string): Outcome token ID to sell (from getPredictionPositionList).
            size (string): Number of shares to sell (positive decimal as string).
            orderType (integer): Order type.
            slippage (string): Maximum acceptable price slippage as decimal (e.g., "0.05" = 5% tolerance).
            eventId (string): Event ID associated with the token.

        Optional args:
            toTokenCode (string): Destination token code; phase 1 is fixed to USDC.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/sell
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_PREDICTION_SELL}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_side_market_list(self, **kwargs):
        """Get related side markets for a sports event

        Required args:
            eventId (string): Sports event ID.

        Optional args:
            sortBy (string): Sort field.
            marketType (integer): Filter by prediction market type.
            limit (integer): Number of records per page.
            pageIndex (integer): Page number starting from 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/side-market-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_SIDE_MARKET_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_group_stage_detail(self, **kwargs):
        """Get group standings and results for a tournament stage

        Required args:
            eventType (integer): Sports event type.

        Optional args:
            groupName (string): Group name used to filter the results.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/sports-group-stage-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_GROUP_STAGE_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_match_list(self, **kwargs):
        """Get match list for a sports prediction event

        Required args:
            eventType (integer): Sports event type.

        Optional args:
            status (integer): Match status filter.
            startTime (integer): Matches starting after this UTC millisecond timestamp.
            endTime (integer): Matches starting before this UTC millisecond timestamp.
            stageCode (string): Filter by tournament stage.
            limit (integer): Number of records per page.
            pageIndex (integer): Page number starting from 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/sports-match-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_MATCH_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_timeline_stages(self, **kwargs):
        """Get tournament timeline stages for a sports event

        Required args:
            eventType (integer): Sports event type.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/sports-timeline-stages
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_TIMELINE_STAGES}",
            query=kwargs,
            auth=True,
        )

    def get_prediction_token_price(self, **kwargs):
        """Get real-time prices for prediction outcome tokens

        Required args:
            tokenIds (array): List of outcome token IDs to query. Maximum 20.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/prediction/token-price
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PREDICTION_TOKEN_PRICE}",
            query=kwargs,
            auth=True,
        )

    def get_asset_detail(self, **kwargs):
        """Get holding details for a specific token including quantity, PnL, and cost basis

        Required args:
            chainCode (string): Blockchain code (ETH, SOL, BSC, etc.).
            tokenAddress (string): Token contract address on chain.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/asset-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_ASSET_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_alpha_asset_list(self, **kwargs):
        """Get user's on-chain token portfolio with holdings, PnL, and market value
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/asset-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_ASSET_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_biz_token_details(self, **kwargs):
        """Get token project details including description, social links, risk flag, and order limits

        Required args:
            chainCode (string): Blockchain code (ETH, SOL, BSC, etc.).
            tokenAddress (string): Token contract address on chain.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/biz-token-details
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_BIZ_TOKEN_DETAILS}",
            query=kwargs,
            auth=True,
        )

    def get_biz_token_list(self, **kwargs):
        """Get on-chain tradable tokens with DEX token codes, risk flags, and order limits

        Optional args:
            tokenTag (integer): 0 all (default), 1 new token, 2 on-chain hot token.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/biz-token-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_BIZ_TOKEN_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_biz_token_price_list(self, **kwargs):
        """Batch query token prices, 24h change, volume, market cap, liquidity, and holders by chain+address

        Required args:
            tokenAddressInfo (array): Token identifiers; maximum 20 items. Each item
                contains required chainCode and tokenAddress string fields.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/biz-token-price-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_BIZ_TOKEN_PRICE_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_alpha_order_list(self, **kwargs):
        """Get trade order history with status, fees, and execution details

        Required args:
            limit (integer): Number of records per page.
            pageIndex (integer): Page number, starting from 1.

        Optional args:
            tradeType (integer): 0 all (default), 1 purchase, 2 redeem.
            tokenCode (string): Filter by token code.
            orderStatus (array): Statuses: 1 processing, 2 success, 3 failed.
            days (integer): Lookback in days, 0-90. Default 0 means 90 days.
            direction (string): Pagination direction: prev or next.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/order-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_ORDER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_pay_token_list(self, **kwargs):
        """Get available payment tokens (USDT, USDC, etc.) with CEX token codes and supported chains

        Required args:
            chainCode (string): Blockchain code (e.g. SOL, MANTLE).
            tokenAddress (string): Token contract address on chain.
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/pay-token-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_PAY_TOKEN_LIST}",
            query=kwargs,
            auth=True,
        )

    def execute_purchase(self, **kwargs):
        """Execute a buy order to purchase on-chain tokens with USDT/USDC, returns order number

        Required args:
            fromTokenCode (string): Payment token code (`CEX_<id>`, e.g. `CEX_1` for USDT). Must match the quote request.
            fromTokenAmount (string): Payment amount (positive decimal as string). Must match the quote request.
            toTokenCode (string): Target on-chain token code (`DEX_<id>`). Must match the quote request.
            slippage (string): Slippage tolerance as decimal.
- `0.005` = 0.5%
- `0.01` = 1%
- `0.05` = 5%

            quoteData (string): Base64-encoded quote data. **Must pass as-is from `/quote` response.**
            gas (string): Estimated gas fee. **Must pass as-is from `/quote` response.**
            quoteMode (integer): Quote mode. Must be consistent with the `/quote` request.
- `0`: Auto
- `1`: Price Priority
- `2`: Success Rate Priority

            correctingCode (string): MD5 checksum for data integrity. **Must pass as-is from `/quote` response.**

        Optional args:
            tenant (string): Optional tenant identifier.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/trade-purchase
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_PURCHASE}",
            query=kwargs,
            auth=True,
        )

    def get_trade_quote(self, **kwargs):
        """Get estimated price, fees, slippage, and gas for an on-chain token trade

        Required args:
            tradeType (integer): Trade type.
- `1`: Purchase (buy on-chain token with payment token)
- `2`: Redeem (sell on-chain token for payment token)

            fromTokenCode (string): Source token code. Format: `CEX_<id>` or `DEX_<id>`.
- Purchase: CEX token code (e.g. `CEX_1` for USDT). Get from `getPayTokenList`.
- Redeem: DEX token code (e.g. `DEX_123`). Get from `getBizTokenList` or `getAssetList`.

            fromTokenAmount (string): Amount to pay (string-formatted positive decimal for precision). Must be greater than 0.
            toTokenCode (string): Target token code. Format: `CEX_<id>` or `DEX_<id>`.
- Purchase: DEX token code (e.g. `DEX_123`). Get from `getBizTokenList`.
- Redeem: CEX token code (e.g. `CEX_1` for USDT). Get from `getPayTokenList`.

        Optional args:
            quoteMode (integer): 0 auto (default), 1 price priority, or 2 success-rate priority.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/trade-quote
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.GET_TRADE_QUOTE}",
            query=kwargs,
            auth=True,
        )

    def execute_alpha_redeem(self, **kwargs):
        """Execute a sell order to redeem on-chain tokens for USDT/USDC, returns order number

        Required args:
            fromTokenCode (string): On-chain token to sell (`DEX_<id>`). Must match the quote request.
            fromTokenAmount (string): Amount to sell (positive decimal as string). Must match the quote request.
            toTokenCode (string): Payment token to receive (`CEX_<id>`, e.g. `CEX_1` for USDT). Must match the quote request.
            slippage (string): Slippage tolerance as decimal.
- `0.005` = 0.5%
- `0.01` = 1%
- `0.05` = 5%

            quoteData (string): Base64-encoded quote data. **Must pass as-is from `/quote` response.**
            gas (string): Estimated gas fee. **Must pass as-is from `/quote` response.**
            quoteMode (integer): Quote mode. Must be consistent with the `/quote` request.
- `0`: Auto
- `1`: Price Priority
- `2`: Success Rate Priority

            correctingCode (string): MD5 checksum for data integrity. **Must pass as-is from `/quote` response.**

        Optional args:
            tenant (string): Optional tenant identifier.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/alpha/trade/trade-redeem
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Alpha.EXECUTE_REDEEM}",
            query=kwargs,
            auth=True,
        )
