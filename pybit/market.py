from enum import Enum


class Market(str, Enum):
    GET_SERVER_TIME = "/v5/market/time"
    GET_KLINE = "/v5/market/kline"
    GET_MARK_PRICE_KLINE = "/v5/market/mark-price-kline"
    GET_INDEX_PRICE_KLINE = "/v5/market/index-price-kline"
    GET_PREMIUM_INDEX_PRICE_KLINE = "/v5/market/premium-index-price-kline"
    GET_INSTRUMENTS_INFO = "/v5/market/instruments-info"
    GET_ORDERBOOK = "/v5/market/orderbook"
    GET_TICKERS = "/v5/market/tickers"
    GET_FUNDING_RATE_HISTORY = "/v5/market/funding/history"
    GET_PUBLIC_TRADING_HISTORY = "/v5/market/recent-trade"
    GET_OPEN_INTEREST = "/v5/market/open-interest"
    GET_HISTORICAL_VOLATILITY = "/v5/market/historical-volatility"
    GET_INSURANCE = "/v5/market/insurance"
    GET_RISK_LIMIT = "/v5/market/risk-limit"
    GET_OPTION_DELIVERY_PRICE = "/v5/market/delivery-price"
    GET_LONG_SHORT_RATIO = "/v5/market/account-ratio"
    GET_PRICE_LIMIT = "/v5/market/price-limit"

    def __str__(self) -> str:
        return self.value
