"""
To use the P2P API, your account must have P2P advertiser access.
See the Bybit P2P API documentation:
https://bybit-exchange.github.io/docs/p2p/guide
"""

from pybit.unified_trading import HTTP
import uuid

session = HTTP(
    testnet=True,
    api_key="...",
    api_secret="...",
)

# Get your P2P profile and advertiser status.
print(session.get_account_information())

# List your own advertisements.
print(session.get_ads_list())

# Fetch one advertisement by ID.
print(session.get_ad_details(itemId="1234567890123456789"))

# List recent and pending P2P orders.
print(session.get_orders(page=1, size=10))
print(session.get_pending_orders(page=1, size=10))

# Fetch one order by ID.
print(session.get_order_details(orderId="1234567890123456789"))

# Upload an image, then send it to the order chat.
uploaded_file = session.upload_chat_file(upload_file="F:/receipt.png")

print(session.send_chat_message(
    orderId="1234567890123456789",
    contentType="pic",
    message=uploaded_file["result"]["url"],
    msgUuid=uuid.uuid4().hex,
))

# Read recent P2P order chat messages.
print(session.get_chat_messages(
    orderId="1234567890123456789",
    size=30,
))
