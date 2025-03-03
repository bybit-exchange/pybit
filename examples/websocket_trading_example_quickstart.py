from pybit.unified_trading import WebSocketTrading
from time import sleep

ws_trading = WebSocketTrading(
    testnet=True,
    api_key="...",
    api_secret="...",
)

def handle_place_order_message(message):
    # Receive the orderId, amend the order, then cancel it.
    print(message)
    sleep(1)
    ws_trading.amend_order(
        handle_amend_order_message,
        category="linear",
        symbol="BTCUSDT",
        order_id=message["data"]["orderId"],
        qty="0.002"
    )
    sleep(1)
    ws_trading.cancel_order(
        handle_cancel_order_message,
        category="linear",
        symbol="BTCUSDT",
        order_id=message["data"]["orderId"]
    )

def handle_amend_order_message(message):
    print(message)

def handle_cancel_order_message(message):
    print(message)

def handle_batch_place_order_message(message):
    print(message)

while True:
    # Simplistic example; place an order every 10 seconds.
    ws_trading.place_order(
        handle_place_order_message,
        category="linear",
        symbol="BTCUSDT",
        side="Buy",
        orderType="Limit",
        price="60000",
        qty="0.001"
    )
    sleep(1)
    # Batch place two orders. Note that batch amend and cancel can be used in
    # the same way – by passing a list of dictionaries to the request parameter.
    request = [
        {
            "symbol": "BTCUSDT",
            "side": "Buy",
            "orderType": "Limit",
            "qty": "0.001",
            "price": "82000",
            "timeInForce": "GTC",
            "positionIdx": 0
        },
        {
            "symbol": "BTCUSDT",
            "side": "Buy",
            "orderType": "Limit",
            "qty": "0.002",
            "price": "82005",
            "timeInForce": "GTC",
            "positionIdx": 0
        }
    ]
    ws_trading.place_batch_order(
        handle_batch_place_order_message,
        category="linear",
        request=request
    )
    sleep(10)
