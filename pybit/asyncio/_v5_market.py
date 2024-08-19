from ._async_http_manager import _V5ASYNCHTTPManager
from ..market import Market


class MarketASYNCHTTP(_V5ASYNCHTTPManager):
    async def get_server_time(self) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/time
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_SERVER_TIME}",
        )

    async def get_kline(self, **kwargs) -> dict:
        """Query the kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type: spot,linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/kline
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_KLINE}",
            query=kwargs,
        )

    async def get_mark_price_kline(self, **kwargs):
        """Query the mark price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/mark-kline
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_MARK_PRICE_KLINE}",
            query=kwargs,
        )

    async def get_index_price_kline(self, **kwargs):
        """Query the index price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/index-kline
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INDEX_PRICE_KLINE}",
            query=kwargs,
        )

    async def get_premium_index_price_kline(self, **kwargs):
        """Retrieve the premium index price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear
            symbol (string): Symbol name
            interval (string): Kline interval

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/preimum-index-kline
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_PREMIUM_INDEX_PRICE_KLINE}",
            query=kwargs,
        )

    async def get_instruments_info(self, **kwargs):
        """Query a list of instruments of online trading pair.

        Required args:
            category (string): Product type. spot,linear,inverse,option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/instrument
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INSTRUMENTS_INFO}",
            query=kwargs,
        )

    async def get_orderbook(self, **kwargs):
        """Query orderbook data

        Required args:
            category (string): Product type. spot, linear, inverse, option
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/orderbook
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_ORDERBOOK}",
            query=kwargs,
        )

    async def get_tickers(self, **kwargs):
        """Query the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

        Required args:
            category (string): Product type. spot,linear,inverse,option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_TICKERS}",
            query=kwargs,
        )

    async def get_funding_rate_history(self, **kwargs):
        """
        Query historical funding rate. Each symbol has a different funding interval.
        For example, if the interval is 8 hours and the current time is UTC 12, then it returns the last funding rate, which settled at UTC 8.
        To query the funding rate interval, please refer to instruments-info.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/history-fund-rate
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_FUNDING_RATE_HISTORY}",
            query=kwargs,
        )

    async def get_public_trade_history(self, **kwargs):
        """Query recent public trading data in Bybit.

        Required args:
            category (string): Product type. spot,linear,inverse,option
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/recent-trade
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_PUBLIC_TRADING_HISTORY}",
            query=kwargs,
        )

    async def get_open_interest(self, **kwargs):
        """Get open interest of each symbol.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            intervalTime (string): Interval. 5min,15min,30min,1h,4h,1d

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/open-interest
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_OPEN_INTEREST}",
            query=kwargs,
        )

    async def get_historical_volatility(self, **kwargs):
        """Query option historical volatility

        Required args:
            category (string): Product type. option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/iv
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_HISTORICAL_VOLATILITY}",
            query=kwargs,
        )

    async def get_insurance(self, **kwargs):
        """
        Query Bybit insurance pool data (BTC/USDT/USDC etc).
        The data is updated every 24 hours.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/insurance
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INSURANCE}",
            query=kwargs,
        )

    async def get_risk_limit(self, **kwargs):
        """Query risk limit of futures

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/risk-limit
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_RISK_LIMIT}",
            query=kwargs,
        )

    async def get_option_delivery_price(self, **kwargs):
        """Get the delivery price for option

        Required args:
            category (string): Product type. option

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/delivery-price
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_OPTION_DELIVERY_PRICE}",
            query=kwargs,
        )

    async def get_long_short_ratio(self, **kwargs):
        """
        Required args:
            category (string): Product type. linear (USDT Perpetual only), inverse
            symbol (string): Symbol name

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/market/long-short-ratio
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_LONG_SHORT_RATIO}",
            query=kwargs,
        )
