"""Async HTTP quickstart.

The example is read-only (get_orderbook, get_wallet_balance). Uncomment the
place_order block to test order submission — but only on testnet, and with
values you're prepared to lose.
"""
import asyncio

from pybit.asyncio.unified_trading import AsyncHTTP

API_KEY = "..."
API_SECRET = "..."


async def main():
    async with AsyncHTTP(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=True,
        record_request_time=True,
    ) as client:
        # Read-only endpoint — no auth needed for public market data.
        # record_request_time=True → 2-tuple (payload, timedelta).
        orderbook, latency = await client.get_orderbook(
            category="linear", symbol="BTCUSDT",
        )
        print(f"orderbook (fetched in {latency.total_seconds()*1000:.1f}ms):", orderbook)

        # Private read-only — requires valid keys.
        balance, _ = await client.get_wallet_balance(accountType="UNIFIED")
        print("balance:", balance)

        # Uncomment to place a live testnet order:
        # order = await client.place_order(
        #     category="linear",
        #     symbol="BTCUSDT",
        #     side="Buy",
        #     orderType="Market",
        #     qty="0.001",
        # )
        # print("order:", order)


if __name__ == "__main__":
    asyncio.run(main())
