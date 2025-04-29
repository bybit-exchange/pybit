from pybit.unified_trading import HTTP

session = HTTP(
    testnet=True,
    api_key="...",
    api_secret="...",
)

print(session.get_orderbook(category="linear", symbol="BTCUSDT"))

print(session.place_order(
    category="linear",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Market",
    qty="0.001",
))
