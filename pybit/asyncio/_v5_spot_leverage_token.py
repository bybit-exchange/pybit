from ._async_http_manager import _V5ASYNCHTTPManager
from ..spot_leverage_token import SpotLeverageToken


class SpotLeverageASYNCHTTP(_V5ASYNCHTTPManager):
    async def get_leveraged_token_info(self, **kwargs):
        """Query leverage token information

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/lt/leverage-token-info
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_LEVERAGED_TOKEN_INFO}",
            query=kwargs,
        )

    async def get_leveraged_token_market(self, **kwargs):
        """Get leverage token market information

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/lt/leverage-token-reference
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_LEVERAGED_TOKEN_MARKET}",
            query=kwargs,
        )

    async def purchase_leveraged_token(self, **kwargs):
        """Purchase levearge token

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L
            ltAmount (string): Purchase amount

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/lt/purchase
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotLeverageToken.PURCHASE}",
            query=kwargs,
            auth=True,
        )

    async def redeem_leveraged_token(self, **kwargs):
        """Redeem leverage token

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L
            quantity (string): Redeem quantity of LT

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/lt/redeem
        """
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotLeverageToken.REDEEM}",
            query=kwargs,
            auth=True,
        )

    async def get_purchase_redemption_records(self, **kwargs):
        """Get purchase or redeem history

        Required args:

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/lt/order-record
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_PURCHASE_REDEMPTION_RECORDS}",
            query=kwargs,
            auth=True,
        )
