from pybit.asyncio._http_manager import _AsyncV5HTTPManager
from pybit.misc import Misc


class AsyncMiscHTTP(_AsyncV5HTTPManager):
    async def get_announcement(self, **kwargs) -> dict:
        """
        Required args:
            locale (string): Language symbol

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/announcement
        """
        return await self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Misc.GET_ANNOUNCEMENT}",
            query=kwargs,
        )

    async def request_demo_trading_funds(self) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/demo
        """
        if not self.demo:
            raise Exception(
                "You must pass demo=True to the pybit HTTP session to use this "
                "method."
            )
        return await self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Misc.REQUEST_DEMO_TRADING_FUNDS}",
            auth=True,
        )
