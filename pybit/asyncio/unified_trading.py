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

__all__ = ["AsyncHTTP"]


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
