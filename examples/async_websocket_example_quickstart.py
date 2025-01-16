import asyncio
from pybit.asyncio.websocket import (
    AsyncWebsocket,
    WSState
)


async def main():
    ws = AsyncWebsocket(
        testnet=True,
        api_key="api_key",
        api_secret="api_secret"
    )
    private_session = ws.order_stream(category="linear")
    async with private_session as active_session:
        while True:
            if active_session.ws_state == WSState.EXITING:
                break
            response = await active_session.recv()
            print(response)
            break

    public_session = ws.kline_stream(symbols=["kline.60.BTCUSDT"], channel_type="linear")
    async with public_session as active_session:
        while True:
            if active_session.ws_state == WSState.EXITING:
                break
            response = await active_session.recv()
            print(response)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
