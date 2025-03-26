"""
    This code is an example of applying Trading Strategy for several Tickers for BACKTEST your ideas.
    The strategy in this code is for demonstration only purposes
    - it outputs OHLCV values,
    - buy at signal1 and signal2 from SMA crossing,
    - then selling on signal3 from SMA and RSI
    Author: Oleg Shpagin, my github: https://github.com/WISEPLAT
    Used libraries: pybit + backtrader + backtrader_bybit
    Here is an example of output: https://www.kaggle.com/olegshpagin/backtest-trading-strategy-for-btc-and-eth-on-bybit
"""

# pip install backtrader_bybit

try:
    from backtrader_bybit import BybitStore
except:
    print("Please install backtrader_bybit: pip install backtrader_bybit")
    exit(1)

import datetime as dt
import backtrader as bt


class UnderOver(bt.Indicator):
    lines = ('underover',)
    params = dict(data2=20)
    plotinfo = dict(plot=True)

    def __init__(self):
        self.l.underover = self.data < self.p.data2             # data under data2 == 1

# Trading System
class RSIStrategy(bt.Strategy):
    """
    Live strategy demonstration with SMA, RSI indicators
    """
    params = (  # Parameters of the trading system
        ('coin_target', ''),
        ('timeframe', ''),
    )

    def __init__(self):
        """Initialization, adding indicators for each ticker"""
        self.orders = {}  # All orders as a dict, for this particularly trading strategy one ticker is one order
        for d in self.datas:  # Running through all the tickers
            self.orders[d._name] = None  # There is no order for ticker yet

        # creating indicators for each ticker
        self.sma1 = {}
        self.sma2 = {}
        self.sma3 = {}
        self.crossover = {}
        self.underover_sma = {}
        self.rsi = {}
        self.underover_rsi = {}
        for i in range(len(self.datas)):
            ticker = list(self.dnames.keys())[i]    # key name is ticker name
            self.sma1[ticker] = bt.indicators.SMA(self.datas[i], period=9)  # SMA1 indicator
            self.sma2[ticker] = bt.indicators.SMA(self.datas[i], period=30)  # SMA2 indicator
            self.sma3[ticker] = bt.indicators.SMA(self.datas[i], period=60)  # SMA3 indicator

            # signal 1 - intersection of a fast SMA from bottom to top of a slow SMA
            self.crossover[ticker] = bt.ind.CrossOver(self.sma1[ticker], self.sma2[ticker])  # crossover SMA1 and SMA2

            # signal 2 - when SMA3 is below SMA2
            self.underover_sma[ticker] = UnderOver(self.sma3[ticker].lines.sma, data2=self.sma2[ticker].lines.sma)

            self.rsi[ticker] = bt.indicators.RSI(self.datas[i], period=20)  # RSI indicator

            # signal 3 - when the RSI is below 30
            self.underover_rsi[ticker] = UnderOver(self.rsi[ticker].lines.rsi, data2=30)

    def next(self):
        """Arrival of a new ticker candle"""
        for data in self.datas:  # Running through all the requested bars of all tickers
            ticker = data._name
            status = data._state  # 0 - Live data, 1 - History data, 2 - None
            _interval = self.p.timeframe

            if status in [0, 1]:
                if status: _state = "False - History data"
                else: _state = "True - Live data"

                print('{} / {} [{}] - Open: {}, High: {}, Low: {}, Close: {}, Volume: {} - Live: {}'.format(
                    bt.num2date(data.datetime[0]),
                    data._name,
                    _interval,  # ticker timeframe
                    data.open[0],
                    data.high[0],
                    data.low[0],
                    data.close[0],
                    data.volume[0],
                    _state,
                ))
                print(f'\t - RSI =', self.rsi[ticker][0])
                print(f"\t - crossover =", self.crossover[ticker].lines.crossover[0])

                coin_target = self.p.coin_target
                print(f"\t - Free balance: {self.broker.getcash()} {coin_target}")

                # signals to open position
                signal1 = self.crossover[ticker].lines.crossover[0]  # signal 1 - intersection of a fast SMA from bottom to top of a slow SMA
                signal2 = self.underover_sma[ticker]  # signal 2 - when SMA3 is below SMA2

                # signals to close position
                signal3 = self.underover_rsi[ticker]  # signal 3 - when the RSI is below 30

                if not self.getposition(data):  # If there is no position
                    if signal1 == 1:
                        if signal2 == 1:
                            # buy
                            free_money = self.broker.getcash()
                            price = data.close[0]  # by closing price
                            size = (free_money / price) * 0.25  # 25% of available funds
                            print("-"*50)
                            print(f"\t - buy {ticker} size = {size} at price = {price}")
                            self.orders[data._name] = self.buy(data=data, exectype=bt.Order.Limit, price=price, size=size)
                            print(f"\t - Order has been submitted {self.orders[data._name].p.tradeid} to buy {data._name}")
                            print("-" * 50)

                else:  # If there is a position
                    if signal3 == 1:
                        # sell
                        print("-" * 50)
                        print(f"\t - Sell by market {data._name}...")
                        self.orders[data._name] = self.close()  # Request to close a position at the market price
                        print("-" * 50)

    def notify_order(self, order):
        """Changing the status of the order"""
        print("*"*50)
        order_data_name = order.data._name  # Name of ticker from order
        self.log(f'Order number {order.ref} {order.info["order_number"]} {order.getstatusname()} {"Buy" if order.isbuy() else "Sell"} {order_data_name} {order.size} @ {order.price}')
        if order.status == bt.Order.Completed:  # If the order is fully executed
            if order.isbuy():  # The order to buy
                self.log(f'Buy {order_data_name} @{order.executed.price:.2f}, Price {order.executed.value:.2f}, Commission {order.executed.comm:.2f}')
            else:  # The order to sell
                self.log(f'Sell {order_data_name} @{order.executed.price:.2f}, Price {order.executed.value:.2f}, Commission {order.executed.comm:.2f}')
                self.orders[order_data_name] = None  # Reset the order to enter the position
        print("*" * 50)

    def notify_trade(self, trade):
        """Changing the position status"""
        if trade.isclosed:  # If the position is closed
            self.log(f'Profit on a closed position {trade.getdataname()} Total={trade.pnl:.2f}, No commission={trade.pnlcomm:.2f}')

    def log(self, txt, dt=None):
        """Print string with date to the console"""
        dt = bt.num2date(self.datas[0].datetime[0]) if not dt else dt  # date or date of the current bar
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Print the date and time with the specified text to the console


if __name__ == '__main__':
    cerebro = bt.Cerebro(quicknotify=True)

    cerebro.broker.setcash(2000)  # Setting how much money
    cerebro.broker.setcommission(commission=0.0015)  # Set the commission - 0.15% ... divide by 100 to remove %

    coin_target = 'USDT'  # the base ticker in which calculations will be performed
    symbol = 'BTC' + coin_target  # the ticker by which we will receive data in the format <CodeTickerBaseTicker>
    symbol2 = 'ETH' + coin_target  # the ticker by which we will receive data in the format <CodeTickerBaseTicker>

    BYBIT_API_KEY = "BYBIT_API_KEY"
    BYBIT_API_SECRET = "BYBIT_API_SECRET"

    if BYBIT_API_KEY == "BYBIT_API_KEY":
        print("Please fill BYBIT_API_KEY and BYBIT_API_SECRET values!")
        exit(1)

    store = BybitStore(
        api_key=BYBIT_API_KEY,
        api_secret=BYBIT_API_SECRET,
        coin_target=coin_target,
        testnet=False)  # Bybit Storage

    # # live connection to Bybit - for Offline comment these two lines
    # broker = store.getbroker()
    # cerebro.setbroker(broker)

    # -----------------------------------------------------------
    # Attention! - Now it's Offline for testing strategies      #
    # -----------------------------------------------------------

    # # Historical 1-minute bars for 10 hours + new live bars / timeframe M1
    # timeframe = "M1"
    # from_date = dt.datetime.now() - dt.timedelta(minutes=60*10)
    # data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol, start_date=from_date, LiveBars=False)  # set True here - if you need to get live bars
    # # data2 = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol2, start_date=from_date, LiveBars=False)  # set True here - if you need to get live bars

    # Historical D1 bars for 365 days + new live bars / timeframe D1
    timeframe = "D"
    from_date = dt.datetime.now() - dt.timedelta(days=365*3)
    data = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol, start_date=from_date, LiveBars=False)  # set True here - if you need to get live bars
    data2 = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol2, start_date=from_date, LiveBars=False)  # set True here - if you need to get live bars

    cerebro.adddata(data)  # Adding data
    cerebro.adddata(data2)  # Adding data

    cerebro.addstrategy(RSIStrategy, coin_target=coin_target, timeframe=timeframe)  # Adding a trading system

    cerebro.run()  # Launching a trading system
    cerebro.plot()  # Draw a chart

    print()
    print("$"*77)
    print(f"Liquidation value of the portfolio: {cerebro.broker.getvalue()}")  # Liquidation value of the portfolio
    print(f"Remaining available funds: {cerebro.broker.getcash()}")  # Remaining available funds
    print("$" * 77)
