from ._http_manager import _V5HTTPManager
from .fmartingalebot import FMartingaleBot


class FMartingaleBotHTTP(_V5HTTPManager):
    def close_f_mart_bot(self, **kwargs):
        """Close a running futures Martingale bot by bot ID.

        Required args:
            bot_id (integer): The bot ID to close, obtained from createFMartBot response.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/futures-martingale/close
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FMartingaleBot.CLOSE_F_MART_BOT}",
            query=kwargs,
            auth=True,
        )

    def create_f_mart_bot(self, **kwargs):
        """Create a new futures Martingale bot with DCA averaging strategy.

        Required args:
            symbol (string): Trading pair symbol (e.g. BTCUSDT).
            martingale_mode (string): Martingale strategy direction.
            leverage (string): Position leverage multiplier as whole number (e.g. '5' means 5x). Must be >= 1.
            price_float_percent (string): Price movement percentage to trigger a position add, as whole number (e.g. '1.5' means add when price moves 1.5% against the position).
            add_position_percent (string): Position add scaling as whole-number percentage of base position size (e.g. '100' means each add equals 1x the base position; '200' means 2x).
            add_position_num (integer): Maximum number of position adds per round.
            init_margin (string): Initial investment amount in quote currency as decimal string (e.g. '1000' for 1000 USDT).
            round_tp_percent (string): Single round take-profit as whole-number percentage (e.g. '3' means close the round when profit reaches 3%).

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/futures-martingale/create
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FMartingaleBot.CREATE_F_MART_BOT}",
            query=kwargs,
            auth=True,
        )

    def get_f_mart_detail(self, **kwargs):
        """Get full details of a futures Martingale bot including PnL, positions, and round progress.

        Required args:
            bot_id (integer): The bot ID to query.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/futures-martingale/get-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FMartingaleBot.GET_F_MART_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_f_mart_limit(self, **kwargs):
        """Validate Martingale bot input parameters and return allowable ranges.

        Required args:
            symbol (string): Trading pair symbol (e.g. BTCUSDT).
            martingale_mode (string): Martingale strategy direction.
            leverage (string): Position leverage multiplier as whole number (e.g. '5' means 5x). Must be >= 1.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/bot/futures-martingale/get-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FMartingaleBot.GET_F_MART_LIMIT}",
            query=kwargs,
            auth=True,
        )
