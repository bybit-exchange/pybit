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
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
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
            total_investment (string): Total investment amount in quote token as decimal string (e.g. '1000' for 1000 USDT).
            cell_number (integer): Number of grid intervals. Must be >= 2.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
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
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
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
            total_investment (string): Total investment amount in quote token as decimal string (e.g. '1000' for 1000 USDT).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Grid.VALIDATE_GRID_INPUT}",
            query=kwargs,
            auth=True,
        )
