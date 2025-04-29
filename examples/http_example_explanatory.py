"""
To see which endpoints are available, check the Bybit API documentation:
https://bybit-exchange.github.io/docs/v5/market/kline
"""

# Import HTTP from the unified_trading module.
from pybit.unified_trading import HTTP

# Set up logging (optional)
import logging
logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")


# You can create an authenticated or unauthenticated HTTP session.
# You can skip authentication by not passing any value for the key and secret.

session = HTTP(
    testnet=True,
    api_key="...",
    api_secret="...",
)

# Get the orderbook of the USDT Perpetual, BTCUSDT
print(session.get_orderbook(category="linear", symbol="BTCUSDT"))
# Note how the "category" parameter determines the type of market to fetch this
# data for. Look at the docstring of the get_orderbook to navigate to the API
# documentation to see the supported categories for this and other endpoints.

# Get wallet balance of the Unified Trading Account
print(session.get_wallet_balance(accountType="UNIFIED"))

# Place an order on that USDT Perpetual
print(session.place_order(
    category="linear",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Market",
    qty="0.001",
))

# Place an order on the Inverse Contract, ETHUSD
print(session.place_order(
    category="inverse",
    symbol="ETHUSD",
    side="Buy",
    orderType="Market",
    qty="1",
))

# Place an order on the Spot market, MNTUSDT
print(session.place_order(
    category="spot",
    symbol="MNTUSDT",
    side="Buy",
    orderType="Market",
    qty="10",
))
