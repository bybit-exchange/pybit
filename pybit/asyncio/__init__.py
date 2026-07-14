"""Async pybit.

**Experimental** — the shape of ``AsyncHTTP`` and ``AsyncWebsocketClient`` may
change in the next minor release. Pin the version if you need stability.

Basic usage::

    from pybit.asyncio.unified_trading import AsyncHTTP

    async with AsyncHTTP(testnet=True, api_key="...", api_secret="...") as client:
        result = await client.get_orderbook(category="linear", symbol="BTCUSDT")
"""
