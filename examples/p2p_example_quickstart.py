from pybit.unified_trading import HTTP

session = HTTP(
    testnet=True,
    api_key="...",
    api_secret="...",
)

print(session.get_account_information())

print(session.get_ads_list())

print(session.get_orders(page=1, size=10))
