from ._http_manager import _V5HTTPManager
from .dca import DCA


class DCAHTTP(_V5HTTPManager):
    def close_dca_bot(self, **kwargs):
        """Close a running DCA bot with a specified settlement mode.

        Required args:
            bot_id (integer): DCA bot ID to close.
            close_mode (integer): Asset settlement mode on close.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/dca/close
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{DCA.CLOSE_DCA_BOT}",
            query=kwargs,
            auth=True,
        )

    def create_dca_bot(self, **kwargs):
        """Create a new DCA (Dollar-Cost Averaging) bot with custom parameters.

        Required args:
            parameters (object): DCA bot configuration parameters.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/dca/create
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{DCA.CREATE_DCA_BOT}",
            query=kwargs,
            auth=True,
        )
