from ._http_manager import _V5HTTPManager
from .rwa import RWA


class RWAHTTP(_V5HTTPManager):
    def get_convert_detail(self, **kwargs):
        """查询 Convert 订单详情

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-detail
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_CONVERT_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_convert_list(self, **kwargs):
        """获取 Convert 交易对列表

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_CONVERT_LIST}",
            query=kwargs,
            auth=True,
        )

    def submit_convert(self, **kwargs):
        """提交 Convert 订单（Mint / Redeem）

        Required args:
            convertType (string): 方向：MINT（正股→Token）/ REDEEM（Token→正股）
            symbol (string): 底层股票代码，如 `AAPL-US`
            inputAmount (string): 输入数量（MINT 时为正股数量，REDEEM 时为 Token 数量）
            frontMultiplier (string): 前端快照的转换比例，服务端会与当前值校验
            requestId (string): 幂等键，字母数字与 `-_`，同一 MM 账号下 24 小时内唯一
            flow (string): 链路类型

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/convert-submit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.SUBMIT_CONVERT}",
            query=kwargs,
            auth=True,
        )

    def get_multiplier_list(self, **kwargs):
        """获取 Multiplier 列表

        Required args:
            current (integer): 当前页码（从 1 开始）
            pageSize (integer): 每页条数，默认 10

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/multiplier-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_MULTIPLIER_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_market_session(self, **kwargs):
        """获取交易日历与市场状态

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/market-session
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_MARKET_SESSION}",
            query=kwargs,
            auth=True,
        )

    def place_stocks_order(self, **kwargs):
        """下单（买入 / 卖出股票）

        Required args:
            symbol (string): 股票代码，如 `TSLA-US`、`AAPL-US`
            quoteToken (string): 计价资产，当前仅支持 `USDC`
            side (string): 方向
            type (string): 订单类型
            timeInForce (string): 订单有效期
            orderTime (integer): 客户端下单毫秒时间戳
            requestId (string): 幂等键，字母数字与 `-_`，同一 MM 账号下 24 小时内唯一

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/place-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.PLACE_STOCKS_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_stocks_order(self, **kwargs):
        """撤单

        Required args:
            orderNo (string): 系统订单号

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/cancel-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RWA.CANCEL_STOCKS_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_stocks_order_detail(self, **kwargs):
        """查询股票订单详情

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/order-detail
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_STOCKS_ORDER_DETAIL}",
            query=kwargs,
            auth=True,
        )

    def get_stocks_positions(self, **kwargs):
        """获取所有正股仓位

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/stocks/positions
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RWA.GET_STOCKS_POSITIONS}",
            query=kwargs,
            auth=True,
        )
