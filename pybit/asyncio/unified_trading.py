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
    AsyncRateLimitHTTP,
    AsyncFiatHTTP,
    AsyncRFQHTTP,
    AsyncP2PHTTP,
    AsyncSpreadHTTP,
)
from pybit.asyncio.ws import (
    AsyncWebsocketClient,
    AsyncWebsocketManager,
)

__all__ = ["AsyncHTTP", "AsyncWebsocketClient", "AsyncWebsocketManager"]


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
    AsyncFiatHTTP,
    AsyncRFQHTTP,
    AsyncRateLimitHTTP,
    AsyncP2PHTTP,
    AsyncSpreadHTTP,
):
    """Aggregated async client for all v5 REST endpoints.

    Experimental — subject to change in the next minor release.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
