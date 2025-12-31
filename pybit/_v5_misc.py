from ._http_manager import _V5HTTPManager
from .misc import Misc


class MiscHTTP(_V5HTTPManager):
    def get_announcement(self, **kwargs) -> dict:
        """
        Required args:
            locale (string): Language symbol

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/announcement
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Misc.GET_ANNOUNCEMENT}",
            query=kwargs,
        )

    def request_demo_trading_funds(self) -> dict:
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
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Misc.REQUEST_DEMO_TRADING_FUNDS}",
            auth=True,
        )

    def get_system_status(self) -> dict:
        """
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/system-status
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Misc.GET_SYSTEM_STATUS}",
        )
