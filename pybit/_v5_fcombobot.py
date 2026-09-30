from ._http_manager import _V5HTTPManager
from .fcombobot import FComboBot


class FComboBotHTTP(_V5HTTPManager):
    def close_combo_bot(self, **kwargs):
        """Close a running futures combo bot by bot ID.

        Required args:
            bot_id (integer): The bot ID to close, obtained from createComboBot response.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FComboBot.CLOSE_COMBO_BOT}",
            query=kwargs,
            auth=True,
        )

    def create_combo_bot(self, **kwargs):
        """Create a new futures combo bot with multi-symbol portfolio and rebalancing.

        Required args:
            leverage (string): Position leverage multiplier as whole number (e.g. '5' means 5x). Must be >= 1.
            init_margin (string): Initial investment amount in quote currency as decimal string (e.g. '1000' for 1000 USDT).
            adjust_position_mode (integer): Position rebalancing trigger mode.
            symbol_settings (array): Per-symbol portfolio configuration (at least one entry required).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FComboBot.CREATE_COMBO_BOT}",
            query=kwargs,
            auth=True,
        )

    def get_combo_detail(self, **kwargs):
        """Get full details of a futures combo bot including PnL, positions, and status.

        Required args:
            bot_id (integer): The bot ID to query.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FComboBot.GET_COMBO_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_combo_limit(self, **kwargs):
        """Validate combo bot input parameters and return allowable ranges.

        Required args:
            leverage (string): Position leverage multiplier as whole number (e.g. '5' means 5x). Must be >= 1.
            init_margin (string): Initial investment amount in quote currency as decimal string (e.g. '1000' for 1000 USDT).
            adjust_position_mode (integer): Position rebalancing trigger mode.
            symbol_settings (array): Per-symbol portfolio configuration.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FComboBot.GET_COMBO_LIMIT}",
            query=kwargs,
            auth=True,
        )
