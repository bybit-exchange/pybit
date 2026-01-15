import asyncio

from pybit.asyncio.unified_trading import AsyncHTTP

API_KEY = "..."
API_SECRET = "..."


async def test():
    async with AsyncHTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=True) as client:
        print(await client.get_orderbook(category="linear", symbol="BTCUSDT"))

        print(await client.place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty="0.001",
        ))

asyncio.run(test())
