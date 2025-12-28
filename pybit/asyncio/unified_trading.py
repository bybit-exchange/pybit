from pybit.asyncio.http import (
    AsyncMiscHTTP,
    AsyncMarketHTTP,
    AsyncTradeHTTP,
    AsyncAccountHTTP,
    AsyncAssetHTTP,
    AsyncPositionHTTP,
    AsyncPreUpgradeHTTP,
    AsyncSpotLeverageHTTP,
    AsyncSpotMarginTradeHTTP,
    AsyncUserHTTP,
    AsyncBrokerHTTP,
    AsyncInstitutionalLoanHTTP,
    AsyncCryptoLoanHTTP,
    AsyncEarnHTTP,
    AsyncRateLimitHTTP
)
from pybit.asyncio.ws import AsyncWebsocketClient

__all__ = ["AsyncHTTP", "AsyncWebsocketClient"]


class AsyncHTTP(
    AsyncMiscHTTP,
    AsyncMarketHTTP,
    AsyncTradeHTTP,
    AsyncAccountHTTP,
    AsyncAssetHTTP,
    AsyncPositionHTTP,
    AsyncPreUpgradeHTTP,
    AsyncSpotLeverageHTTP,
    AsyncSpotMarginTradeHTTP,
    AsyncUserHTTP,
    AsyncBrokerHTTP,
    AsyncInstitutionalLoanHTTP,
    AsyncCryptoLoanHTTP,
    AsyncEarnHTTP,
    AsyncRateLimitHTTP
):
    ...
