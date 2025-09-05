from pybit.unified_trading import WebSocket
from time import sleep

ws = WebSocket(
    testnet=True,
    channel_type="linear",
)

def handle_message(message):
    print(message["topic"],message["data"]["symbol"],message["data"]["lastPrice"])

ws.ticker_stream("BTCUSDT", handle_message)
ws.ticker_stream("ETHUSDT", handle_message)

count=0
while True:
    count+=1
    sleep(1)

    if count==3:
        topics=ws.get_subscription_topics() # Get all subscribed topics

        topic = [topic for topic in topics if "BTCUSDT" in topic][0] # Find topic that includes BTCUSDT

        ws.unsubscribe(topic) # Unsubscribe

        print("unsubscribed from",topic)
