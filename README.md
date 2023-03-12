# pybit
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Build Status](https://img.shields.io/pypi/pyversions/pybit)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/pypi/v/pybit)](https://pypi.org/project/pybit/)
[![Build Status](https://travis-ci.org/verata-veritatis/pybit.svg?branch=master)](https://travis-ci.org/verata-veritatis/pybit)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Official Python3 API connector for Bybit's HTTP and WebSockets APIs.

## Table of Contents

- [About](#about)
- [Development](#development)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
  * [Market Data Endpoints](#market-data-endpoints)
    + [Advanced Data](#advanced-data)
  * [Account Data Endpoints](#account-data-endpoints)
    + [Active Orders](#active-orders)
    + [Conditional Orders](#conditional-orders)
    + [Position](#position)
    + [Market Maker Protection](#market-maker-protection)
    + [Risk Limit](#risk-limit)
    + [Funding](#funding)
    + [API Key Info](#api-key-info)
    + [LCP Info](#lcp-info)
  * [Wallet Data Endpoints](#wallet-data-endpoints)
  * [API Data Endpoints](#api-data-endpoints)
  * [Account Asset Endpoints](#account-asset-endpoints)
  * [WebSocket](#websocket)
    * [Futures](#futures)
      + [Public Topics](#public-topics)
      + [Private Topics](#private-topics)
    + [Spot](#spot)
      + [Public Topics V1](#public-topics-v1)
      + [Public Topics V2](#public-topics-v2)
      + [Private Topics](#private-topics-spot)
- [Contact](#contact)
- [Contributors](#contributors)
- [Donations](#donations)

## About
Put simply, `pybit` (Python + Bybit) is the official lightweight one-stop-shop module for the Bybit HTTP and WebSocket APIs. Originally created by [Verata Veritatis](https://github.com/verata-veritatis), it's now maintained by Bybit employees - however, you're still welcome to contribute!

It was designed with the following vision in mind:

> I was personally never a fan of auto-generated connectors that used a mosh-pit of various modules you didn't want (sorry, `bravado`) and wanted to build my own Python3-dedicated connector with very little external resources. The goal of the connector is to provide traders and developers with an easy-to-use high-performing module that has an active issue and discussion board leading to consistent improvements.

## Development
`pybit` is being actively developed, and new Bybit API changes should arrive on `pybit` very quickly. `pybit` uses `requests` and `websocket-client` for its methods, alongside other built-in modules. Anyone is welcome to branch/fork the repository and add their own upgrades. If you think you've made substantial improvements to the module, submit a pull request and we'll gladly take a look.

## Installation (working for v5)
`pybit` requires Python 3.9 or higher. The module can be installed with `pip`:
```
pip install git+https://github.com/ervuks/pybit.git@v5-only
```

## Basic Usage
You can retrieve a specific market like so:
```python
from pybit import inverse_perpetual
```
Create an HTTP session and connect via WebSocket for Inverse on mainnet:
```python
session = inverse_perpetual.HTTP(
    endpoint='https://api.bybit.com', 
    api_key='...',
    api_secret='...'
)
ws = inverse_perpetual.WebSocket(
    test=False,
    api_key="...",
    api_secret="..."
)
```
Information can be sent to, or retrieved from, the Bybit APIs:

```python
# Get orderbook.
session.orderbook(symbol='BTCUSD')

# Create five long orders.
orders = [{
    "symbol": "BTCUSD",
    "order_type": "Limit",
    "side": "Buy",
    "qty": 100,
    "price": i,
    "time_in_force": "GoodTillCancel"
} for i in [5000, 5500, 6000, 6500, 7000]]

# Submit the orders in bulk.
session.place_active_order_bulk(orders)


# Check on your order and position through WebSocket.
def handle_orderbook(message):
    print(message)


def handle_position(message):
    print(message)


ws.orderbook_stream(handle_orderbook, "BTCUSD")
ws.position_stream(handle_position)

while True:
    # Run your main trading strategy here
    pass  # To avoid CPU utilisation, use time.sleep(1)
```
Check out the example python files or the list of endpoints below for more information on available
endpoints and methods. Usage examples on the `HTTP` methods can
be found at:
- https://github.com/bybit-exchange/pybit/blob/master/examples/http_example.py

Usage examples on the `WebSocket` methods can be found at:
- https://github.com/bybit-exchange/pybit/blob/master/examples/websocket_example.py

### Market Data Endpoints

| Endpoint                          | Method |
| -------------                     | ------------- |
| Orderbook                         | `orderbook()`  |
| Query Kline                       | `query_kline()` |
| Latest Information for Symbol     | `latest_information_for_symbol()` |
| Public Trading Records            | `public_trading_records()` |
| Query Symbol                      | `query_symbol()` |
| Liquidated Orders                 | `liquidated_orders()` |
| Query Mark Price Kline            | `query_mark_price_kline()` |
| Open Interest                     | `open_interest()` |
| Delivery Price (USDC)         | `delivery_price()`                |
| Last 500 Trades (USDC)        | `last_500_trades()`               |

#### Advanced Data

| Endpoint              | Method |
| -------------         | ------------- |
| Query Kline           | `query_kline()` |
| Latest Big Deal       | `latest_big_deal()` |
| Long Short Ratio      | `long_short_ratio()` |

### Account Data Endpoints

#### Active Orders

| Endpoint                                | Method                               |
| --------------------------------------- | ------------------------------------ |
| Place Active Order                      | `place_active_order()`               |
| Get Active Order                        | `get_active_order()`                 |
| Cancel Active Order                     | `cancel_active_order()`              |
| Cancel All Active Orders                | `cancel_all_active_orders()`         |
| Replace Active Order                    | `replace_active_order()`             |
| Query Active Order                      | `query_active_order()`               |
| Batch Place Active Orders (USDC)        | `batch_place_active_orders()`         |
| Fast Cancel Active Order (Spot)         | `fast_cancel_active_order()`         |
| Batch Cancel Active Order (Spot, USDC)  | `batch_cancel_active_order()`        |
| Batch Fast Cancel Active Order (Spot)   | `batch_fast_cancel_active_order()`   |
| Batch Cancel Active Order By IDs (Spot) | `batch_cancel_active_order_by_ids()` |
| Batch Replace Active Orders (USDC)      | `batch_replace_active_orders()`      |

#### Conditional Orders

| Endpoint                          | Method |
| -------------                     | ------------- |
| Place Conditional Order           | `place_conditional_order()`  |
| Get Conditional Order             | `get_conditional_order()`  |
| Cancel Conditional Order          | `cancel_conditional_order()`  |
| Cancel All Conditional Orders     | `cancel_all_conditional_orders()`  |
| Replace Conditional Order         | `replace_conditional_order()`  |
| Query Conditional Order           | `query_conditional_order()` |

#### Position

| Endpoint                                              | Method |
| -------------                                         | ------------- |
| My Position                                           | `my_position()`  |
| Set Auto Add Margin (Linear)                          | `set_auto_add_margin()`  |
| Cross/Isolated Margin Switch (Linear)                 | `cross_isolated_margin_switch()`  |
| Full/Partial Position SL/TP Switch                    | `full_partial_position_tp_sl_switch` |
| Add/Reduce Margin (Linear)                            | `add_reduce_margin()` |
| Set Trading-Stop                                      | `set_trading_stop()`  |
| Set Leverage                                          | `set_leverage()`  |
| User Leverage (deprecated)                            | `user_leverage()` |
| User Trade Records                                    | `user_trade_records()`  |
| Closed Profit and Loss                                | `closed_profit_and_loss()` |
| Query Trading Fee Rate                                | `query_trading_fee_rate()` |
| Query Delivery History (USDC)         | `query_delivery_history()`           |
| Query Position Expiration Date (USDC) | `query_position_expiration_date()`   |

#### Market Maker Protection

Only available for the USDC API.

| Endpoint   | Method         |
| ---------- | -------------- |
| Query MMP  | `query_mmp`()  |
| Modify MMP | `modify_mmp`() |
| Reset MMP  | `reset_mmp`()  |

#### Risk Limit

| Endpoint                      | Method |
| -------------                 | ------------- |
| Get Risk Limit                | `my_position()`  |
| Set Risk Limit (Inverse)      | `set_auto_add_margin()`  |

#### Funding

| Endpoint                                      | Method |
| -------------                                 | ------------- |
| Get the Last Funding Rate                     | `get_the_last_funding_rate()`  |
| My Last Funding Fee                           | `my_last_funding_fee()`  |
| Predicted Funding Rate and My Funding Fee     | `predicted_funding_rate()` |

#### API Key Info

| Endpoint          | Method |
| -------------     | ------------- |
| API Key Info      | `api_key_info()`  |

#### LCP Info

| Endpoint          | Method |
| -------------     | ------------- |
| LCP Info          | `lcp_info()`  |

### Wallet Data Endpoints

| Endpoint                  | Method |
| -------------             | ------------- |
| Get Wallet Balance        | `get_wallet_balance()`  |
| Wallet Fund Records       | `wallet_fund_records()`  |
| Withdraw Records          | `withdraw_records()`  |
| Asset Exchange Records    | `asset_exchange_records()` |
| Get Asset Info (USDC)  | `get_asset_info()`         |
| Get Margin Mode (USDC) | `get_margin_mode()`        |

### API Data Endpoints

| Endpoint           | Method |
| -------------      | ------------- |
| Server Time        | `server_time()`  |
| Announcement       | `announcement()`  |

### Account Asset Endpoints

| Endpoint                       | Method                             |
| ------------------------------ | ---------------------------------- |
| Create Internal Transfer       | `create_internal_transfer()`       |
| Create Subaccount Transfer     | `create_subaccount_transfer()`     |
| Query Transfer List            | `query_transfer_list()`            |
| Query Subaccount Transfer List | `query_subaccount_transfer_list()` |
| Query Subaccount List          | `query_subaccount_list()`          |
| Enable Universal Transfer      | `enable_universal_transfer()`      |
| Create Universal Transfer      | `create_universal_transfer()`      |
| Query Universal Transfer List  | `query_universal_transfer_list()`  |
| Query Supported Deposit List   | `query_supported_deposit_list()`   |
| Query Deposit Records          | `query_deposit_records()`          |
| Query Withdraw Records         | `query_withdraw_records()`         |
| Query Coin Info                | `query_coin_info()`                |
| Query Asset Info               | `query_asset_info()`               |
| Withdraw                       | `withdraw()`                       |
| Cancel Withdrawal              | `cancel_withdrawal()`              |
| Query Deposit Address          | `query_deposit_address()`          |

### pybit Custom Endpoints

| Endpoint                          | Method |
| -------------                     | ------------- |
| Place Active Order (Bulk)         | `place_active_order_bulk()`  |
| Cancel Active Order (Bulk)        | `cancel_active_order_bulk()`  |
| Place Conditional Order (Bulk)    | `place_conditional_order_bulk()`  |
| Cancel Conditional Order (Bulk)   | `cancel_conditional_order_bulk()`  |
| Close Position                    | `close_position()` |

### WebSocket

To see comprehensive examples of how to subscribe to the futures and spot websockets, check the [examples file](https://github.com/bybit-exchange/pybit/blob/master/examples/websocket_example.py).

## Contact
You can reach out for support on the [BybitAPI Telegram](https://t.me/BybitAPI) group chat.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/verata-veritatis"><img src="https://avatars0.githubusercontent.com/u/9677388?v=4" width="100px;" alt=""/><br /><sub><b>verata-veritatis</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=verata-veritatis" title="Code">💻</a> <a href="https://github.com/verata-veritatis/pybit/commits?author=verata-veritatis" title="Documentation">📖</a></td>
     <td align="center"><a href="https://github.com/APF20"><img src="https://avatars0.githubusercontent.com/u/74583612?v=4" width="100px;" alt=""/><br /><sub><b>APF20</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=APF20" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/cameronhh"><img src="https://avatars0.githubusercontent.com/u/30434979?v=4" width="100px;" alt=""/><br /><sub><b>Cameron Harder-Hutton</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=cameronhh" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/tomcru"><img src="https://avatars0.githubusercontent.com/u/35841182?v=4" width="100px;" alt=""/><br /><sub><b>Tom Rumpf</b></sub></a><br /><a href="https://github.com/verata-veritatis/pybit/commits?author=tomcru" title="Code">💻</a></td>
     <td align="center"><a href="https://github.com/tconley"><img src="https://avatars1.githubusercontent.com/u/1893207?v=4" width="100px;" alt=""/><br /><sub><b>Todd Conley</b></sub></a><br /><a href="https://github.com/tconley/pybit/commits?author=tconley" title="Ideas">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
