# pybit
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
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
- [Usage](#usage)
- [Contact](#contact)
- [Contributors](#contributors)
- [Donations](#donations)

## About
Put simply, `pybit` (Python + Bybit) is the official lightweight one-stop-shop module for the Bybit HTTP and WebSocket APIs. Originally created by [Verata Veritatis](https://github.com/verata-veritatis), it's now maintained by Bybit employees - however, you're still welcome to contribute!

It was designed with the following vision in mind:

> I was personally never a fan of auto-generated connectors that used a mosh-pit of various modules you didn't want (sorry, `bravado`) and wanted to build my own Python3-dedicated connector with very little external resources. The goal of the connector is to provide traders and developers with an easy-to-use high-performing module that has an active issue and discussion board leading to consistent improvements.

## Development
`pybit` is being actively developed, and new Bybit API changes should arrive on `pybit` very quickly. `pybit` uses `requests` and `websocket-client` for its methods, alongside other built-in modules. Anyone is welcome to branch/fork the repository and add their own upgrades. If you think you've made substantial improvements to the module, submit a pull request and we'll gladly take a look.

## Installation
`pybit` requires Python 3.9.1 or higher. The module can be installed manually or via [PyPI](https://pypi.org/project/pybit/) with `pip`:
```
pip install pybit
```

## Usage
You can retrieve a specific market like so:
```python
from pybit.unified_trading import HTTP
```
Create an HTTP session and connect via WebSocket for Inverse on mainnet:
```python
session = HTTP(
    testnet=False,
    api_key="...",
    api_secret="...",
)
```
Information can be sent to, or retrieved from, the Bybit APIs:

```python
# Get the orderbook of the USDT Perpetual, BTCUSDT
session.get_orderbook(category="linear", symbol="BTCUSDT")

# Create five long USDC Options orders.
# (Currently, only USDC Options support sending orders in bulk.)
payload = {"category": "option"}
orders = [{
  "symbol": "BTC-30JUN23-20000-C",
  "side": "Buy",
  "orderType": "Limit",
  "qty": "0.1",
  "price": i,
} for i in [15000, 15500, 16000, 16500, 16600]]

payload["request"] = orders
# Submit the orders in bulk.
session.place_batch_order(payload)
```
Check out the example python files or the list of endpoints below for more information on available
endpoints and methods. Usage examples on the `HTTP` methods can
be found in the [examples folder](https://github.com/bybit-exchange/pybit/tree/master/examples).


## Contact
You can reach out for support on the [BybitAPI Telegram](https://t.me/BybitAPI) group chat.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/verata-veritatis"><img src="https://avatars0.githubusercontent.com/u/9677388?v=4?s=100" width="100px;" alt="verata-veritatis"/><br /><sub><b>verata-veritatis</b></sub></a><br /><a href="https://github.com/bybit-exchange/pybit/commits?author=verata-veritatis" title="Code">💻</a> <a href="https://github.com/bybit-exchange/pybit/commits?author=verata-veritatis" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kevinwon96"><img src="https://avatars.githubusercontent.com/u/107445491?v=4?s=100" width="100px;" alt="kevinwon96"/><br /><sub><b>kevinwon96</b></sub></a><br /><a href="https://github.com/bybit-exchange/pybit/commits?author=kevinwon96" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
