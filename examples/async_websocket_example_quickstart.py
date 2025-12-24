import asyncio

from pybit.asyncio.ws import AsyncWebsocketClient


API_KEY = "..."
API_SECRET = "..."


async def test_public():
    client = AsyncWebsocketClient(testnet=True, channel_type="linear")
    stream = client.futures_kline_stream(symbols=["kline.60.BTCUSDT", "kline.60.ETHUSDT", "kline.60.SOLUSDT"])
    async with stream as ws:
        while True:
            print(await ws.recv())


asyncio.run(test_public())


async def test_private():
    client = AsyncWebsocketClient(
        testnet=True,
        channel_type="private",
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    stream = client.user_futures_stream()
    async with stream as ws:
        while True:
            print(await ws.recv())


asyncio.run(test_private())
