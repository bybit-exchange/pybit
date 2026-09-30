from ._http_manager import _V5HTTPManager
from .fgridbot import FGridBot


class FGridBotHTTP(_V5HTTPManager):
    def close_f_grid_bot(self, **kwargs):
        """Close a running futures grid bot by bot ID.

        Required args:
            bot_id (integer): The bot ID to close, obtained from createFGridBot response.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FGridBot.CLOSE_F_GRID_BOT}",
            query=kwargs,
            auth=True,
        )

    def create_f_grid_bot(self, **kwargs):
        """Create a new futures grid trading bot with specified parameters.

        Required args:
            symbol (string): Trading pair symbol (e.g. BTCUSDT).
            grid_mode (integer): Grid strategy direction.
            min_price (string): Lower price bound of the grid range.
            max_price (string): Upper price bound of the grid range.
            cell_number (integer): Number of grid levels (minimum 2).
            leverage (string): Position leverage multiplier as whole number (e.g. '5' means 5x leverage). Must be >= 1.
            grid_type (integer): Grid spacing type.
            total_investment (string): Initial investment amount in quote currency as decimal string (e.g. '1000' for 1000 USDT).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FGridBot.CREATE_F_GRID_BOT}",
            query=kwargs,
            auth=True,
        )

    def get_f_grid_detail(self, **kwargs):
        """Get full details of a futures grid bot including PnL, positions, and status.

        Required args:
            bot_id (integer): The bot ID to query.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FGridBot.GET_F_GRID_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def validate_f_grid_input(self, **kwargs):
        """Validate futures grid bot input parameters and return allowable ranges.

        Required args:
            symbol (string): Trading pair symbol (e.g. BTCUSDT).
            cell_number (integer): Number of grid levels (minimum 2).
            min_price (string): Lower price bound of the grid range.
            max_price (string): Upper price bound of the grid range.
            leverage (string): Position leverage, must be >= 1 (e.g. '5').
            grid_type (integer): Grid spacing type.
            grid_mode (integer): Grid strategy direction.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FGridBot.VALIDATE_F_GRID_INPUT}",
            query=kwargs,
            auth=True,
        )
