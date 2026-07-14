"""Async WebSocket quickstart.

The async WS client uses a pull model — call ``await ws.recv()`` in a loop
rather than passing a callback. ``recv()`` returns ``None`` on timeout (no
frame within the recv window), so guard for it.

Run either ``main_public`` or ``main_private`` from the command line, e.g.::

    python async_websocket_example_quickstart.py public
    python async_websocket_example_quickstart.py private
"""
import asyncio
import sys

from pybit.asyncio.ws import AsyncWebsocketClient


API_KEY = "..."
API_SECRET = "..."


async def main_public():
    client = AsyncWebsocketClient(testnet=True, channel_type="linear")
    stream = client.futures_kline_stream(
        symbols=["kline.60.BTCUSDT", "kline.60.ETHUSDT", "kline.60.SOLUSDT"],
    )
    async with stream as ws:
        try:
            while True:
                msg = await ws.recv()
                if msg is None:
                    continue
                print(msg)
        except KeyboardInterrupt:
            print("Interrupted; closing.")


async def main_private():
    client = AsyncWebsocketClient(
        testnet=True,
        channel_type="private",
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    stream = client.user_futures_stream()
    async with stream as ws:
        try:
            while True:
                msg = await ws.recv()
                if msg is None:
                    continue
                print(msg)
        except KeyboardInterrupt:
            print("Interrupted; closing.")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "public"
    if mode == "private":
        asyncio.run(main_private())
    else:
        asyncio.run(main_public())
