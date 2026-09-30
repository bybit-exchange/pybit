from ._http_manager import _V5HTTPManager
from .grid import Grid


class GridHTTP(_V5HTTPManager):
    def close_grid_bot(self, **kwargs):
        """Close a running spot grid bot with a specified settlement mode.

        Required args:
            grid_id (integer): Grid bot ID to close.
            close_mode (integer): Asset settlement mode on close.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/spot-grid/close
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Grid.CLOSE_GRID_BOT}",
            query=kwargs,
            auth=True,
        )

    def create_grid_bot(self, **kwargs):
        """Create a new spot grid trading bot.

        Required args:
            symbol (string): Trading pair symbol in uppercase, e.g. "BTCUSDT".
            max_price (string): Upper bound of the grid price range (decimal string).
            min_price (string): Lower bound of the grid price range (decimal string).
            cell_number (integer): Number of grid intervals. Must be >= 2.

        Optional args:
            invest_mode (integer): 0 for quote only (default), 1 for base only,
                or 2 for base and quote.
            base_investment (string): Amount of the base asset to invest.
                Required when invest_mode is 1 or 2.
            quote_investment (string): Amount of the quote asset to invest.
                Required when invest_mode is 0 or 2.
            entry_price (string): Entry price for the bot.
            stop_loss_price (string): Stop-loss trigger price.
            take_profit_price (string): Take-profit trigger price.
            ts_percent (string): Trailing-stop percentage.
            enable_trailing (boolean): Whether trailing is enabled.
            limit_up_price (string): Upper price limit for trailing.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/spot-grid/create
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Grid.CREATE_GRID_BOT}",
            query=kwargs,
            auth=True,
        )

    def query_grid_detail(self, **kwargs):
        """Query full details of a specific grid bot by grid_id.

        Required args:
            grid_id (integer): The grid bot ID, obtained from createGridBot response or grid list.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/spot-grid/get-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Grid.QUERY_GRID_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def validate_grid_input(self, **kwargs):
        """Validate spot grid bot parameters before creation.

        Required args:
            symbol (string): Trading pair symbol in uppercase, e.g. "BTCUSDT".
            cell_number (integer): Number of grid intervals. Must be >= 2.
            min_price (string): Lower bound of the grid price range (decimal string).
            max_price (string): Upper bound of the grid price range (decimal string). Must be greater than min_price.

        Optional args:
            invest_mode (integer): 0 for quote only (default), 1 for base only,
                or 2 for base and quote.
            base_investment (string): Amount of the base asset to invest.
                Required when invest_mode is 1 or 2.
            quote_investment (string): Amount of the quote asset to invest.
                Required when invest_mode is 0 or 2.
            stop_loss (string): Stop-loss setting to validate.
            take_profit (string): Take-profit setting to validate.
            entry_price (string): Entry price for validation.
            ts_percent (string): Trailing-stop percentage.
            enable_trailing (boolean): Whether trailing is enabled.
            limit_up_price (string): Upper price limit for trailing.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/spot-grid/validate-input
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Grid.VALIDATE_GRID_INPUT}",
            query=kwargs,
            auth=True,
        )
