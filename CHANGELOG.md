# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [5.10.1] - 2025-04-08

### Fixed
- HTTP args `retry_codes` and `ignore_codes`


## [5.10.0] - 2025-03-13

### Added
- `all_liquidation_stream` WebSocket topic.
- Batch WebSocket order methods: `place_batch_order`, `amend_batch_order`, `cancel_batch_order`
- HTTP API methods for [Convert](https://bybit-exchange.github.io/docs/v5/asset/convert/guideline), [Earn](https://bybit-exchange.github.io/docs/v5/earn/product-info), and [Crypto Loan](https://bybit-exchange.github.io/docs/v5/crypto-loan/collateral-coin).

### Changed
- Renamed the arg `callback_function` in the WebSocket class to `_callback_function` as it's intended to be private and is not useful to the user. This is not the `callback_function` arg you pass when subscribing to a WebSocket topic. ([https://github.com/bybit-exchange/pybit/issues/270](#270))
- Allow passing `None` as a value to an HTTP request, which results in the parameter being removed the final request sent.

### Deprecated
- `liquidation_stream` WebSocket topic.


## [5.9.0] - 2025-01-27

Thanks goes to [Kamsby](https://github.com/Kamsby), [kolya5544](https://github.com/kolya5544), and [LordGhostX](https://github.com/LordGhostX) for contributing to this release.

### Added
- Add `fast_execution_stream` WebSocket
- Add `tld` arg to WebSocket. TLD stands for top-level domain.
- Add `delete_sub_uid` and `get_all_sub_api_keys` – user-related HTTP endpoints
- Add `spot_margin_trade_get_historical_interest_rate` – a spot margin HTTP endpoint
- Add `add_or_reduce_margin` – a position HTTP endpoint
- Add `get_transferable_amount` – an account-related HTTP endpoint to complement `get_wallet_balance`
- Add `get_exchange_broker_earnings` (see Deprecated)

### Deprecated
- `get_broker_earnings` HTTP endpoint. Instead use `get_exchange_broker_earnings`.

### Removed
- All modules under the `legacy` subpackage. All these APIs are offline by this point and their functionality is covered by the V5 API / Unified Trading Account.


## [5.8.0] - 2024-06-26
### Added
- [WebSocket Trading](https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline) support
- Add `get_contract_transaction_log`


## [5.7.0] - 2024-04-11
### Added
- [Demo Trading](https://bybit-exchange.github.io/docs/v5/demo) support 
- Add methods for the [Institutional Loan](https://bybit-exchange.github.io/docs/v5/otc/margin-product-info) endpoints
- Add [Account](https://bybit-exchange.github.io/docs/v5/account/wallet-balance) methods `repay_liability()`, `set_collateral_coin()`, `batch_set_collateral_coin()`
- `tld` arg for users in The Netherlands and Hong Kong for `HTTP` sessions

### Fixed
- Options WebSocket failing to maintain connection (https://github.com/bybit-exchange/pybit/issues/164)


## [5.6.1] - 2023-10-09
### Changed
- Improved the IP rate limit error message to indicate that an HTTP status code 403 may also mean that the IP address was identified as being from the USA – all requests from USA IPs are [banned](https://t.me/BybitAPI/180420) by Bybit.


## [5.6.0] - 2023-09-28
### Added
- Add RSA authentication for HTTP and WebSocket (choose "Self-generated API Keys" when [creating](https://testnet.bybit.com/app/user/api-management) an API key)
  - To use it, pass `rsa_authentication=True` along with your `api_key` and `api_secret`
    - Your `api_key` is given to you after inputting your public key (RSA) into Bybit's API management system
    - Your `api_secret` is the private key (RSA) you generate
  - Learn more [here](https://www.bybit.com/en-US/help-center/bybitHC_Article?id=000001923&language=en_US)
  - See examples files: [HTTP](https://github.com/bybit-exchange/pybit/blob/master/examples/http_example_rsa_authentication.py) and [WebSocket](https://github.com/bybit-exchange/pybit/blob/master/examples/websocket_example_rsa_authentication.py)
- Add the `HTTP` method `get_server_time()`
- Add `HTTP` methods for spot margin trading
- Add `HTTP` method `get_long_short_ratio()`
- Add optional `private_auth_expire` arg for WebSocket (https://github.com/bybit-exchange/pybit/pull/154)

### Deprecated
- The `HTTP` method `enable_universal_transfer_for_sub_uid()`

### Fixed
- Improve `close_position` logic

## [5.5.0] - 2023-07-17
### Added
- `helpers.py` which includes the `Helpers` class and the `close_position` method, which can be imported and employed like so:
```python
from pybit.helpers import Helpers
my_helper = Helpers(session)  # your HTTP session object (eg, from pybit.unified_trading import HTTP)
print(my_helper.close_position(category="linear", symbol="BTCUSDT"))
```

## [5.4.0] - 2023-06-23
### Added
- The following new endpoints to `unified_trading`:
  - `get_broker_earnings`
  - `get_announcement`
  - `get_pre_upgrade_order_history`
  - `get_pre_upgrade_trade_history`
  - `get_pre_upgrade_closed_pnl`
  - `get_pre_upgrade_transaction_log`
  - `get_pre_upgrade_option_delivery_record`
  - `get_pre_upgrade_usdc_session_settlement`
  - `get_affiliate_user_info`
  - `get_uid_wallet_type`


## [5.3.0] - 2023-05-19
### Added
- Multiple symbol support for WebSocket topics (pass `symbol` as a list)
- Extra logging (log response headers) when passing `log_requests=True`
- Argument `return_response_headers` for `HTTP` to allow returning the response headers to the user

### Modified
- Add response headers to exceptions

### Fixed
- Update PyPI package's python version so that only =>3.9 is supported to prevent the error: `TypeError: 'type' object is not subscriptable`
- Fix API rate limit handling
- Remove unnecessary `print` statements in two methods


## [5.2.0] - 2023-04-18
### Added
- New asset endpoints: `set_deposit_account()`, `get_internal_deposit_records()`, `get_withdrawable_amount()`

### Fixed
- Ensure that `legacy` submodule is packaged by `setup.py`
- Fix non-UTA (normal account) spot margin trading endpoints
- Fix wrong request method for `set_dcp()`


## [5.1.1] - 2023-04-06
### Added
- HTTP endpoints to the `copy_trading` module

### Modified
- Docstrings in the `copy_trading` module to make it easier to find the API documentation for reference
- Example files

### Fixed
- `ticker_stream` method in the `unified_trading` module, which was subscribing to the wrong WebSocket topic


## [5.0.0] - 2023-04-03
This version upgrades pybit to Bybit's [version 5 (v5) APIs](https://bybit-exchange.github.io/docs/v5/intro). It supports both [Unified Trading Accounts](https://www.bybit.com/en-US/help-center/s/article/Introduction-to-Bybit-Unified-Trading-Account) (UTA) and non-UTA accounts. Bybit is not expected to develop any more major API versions in the future, so Bybit's v5 API (and subsequently, pybit's 5.0.0) is expected to be supported in the long-term.

See the [examples folder](https://github.com/bybit-exchange/pybit/tree/master/examples) for examples on how to interact with the latest modules.

### Added
- Bybit's v5 HTTP and WebSocket APIs in the `unified_trading` module. See what markets All-In-One V5 API supports in the [upgrade guide](https://bybit-exchange.github.io/docs/v5/upgrade-guide).

### Modified
- Non-v5 modules like `copy_trading`, `usdc_options`, and `usdc_perpetuals` to continue to work from a `legacy` subpackage. Import like so: `from pybit.legacy.copy_trading import HTTP
`. These modules are maintained because they are currently not supported by the v5 API; see the [upgrade guide](https://bybit-exchange.github.io/docs/v5/upgrade-guide).

### Removed
- Various legacy modules which have been superseded by the v5 API via the `unified_trading` module

### Fixed
- Tests for V5 endpoints


## [3.0.0rc5] - 2023-02-02
### Added
- `copy_trading` module for the [Copy Trading](https://bybit-exchange.github.io/docs/copy_trading/) HTTP API and WebSocket

### Modified
- `requirements.txt` to require the latest version of `websocket-client`: `1.5.0`.
  - If you are facing any problems with the WebSocket, ensure you upgrade to the right version of the dependency and try again. Upgrade like so: `python -m pip install -r requirements.txt`
- WebSocket pings (again)


## [3.0.0rc4] - 2023-01-31
### Modified
- How WebSocket pings are sent in an effort to keep connections open longer

## [3.0.0rc3] - 2023-01-27
### Fixed
- Failure to resubscribe to private spot topics when reconnecting WebSocket

### Modified
- WebSocket error handling

## [3.0.0rc2] - 2023-01-05
### Fixed
- Failure to pass request parameters in certain methods


## [3.0.0rc1] - 2023-01-04
### Fixed
- Wrong endpoint paths in `spot`

### Modified
- Refactored WebSocket's `test` arg to `testnet`
- Hardcoded WebSocket arguments into the child class the user accesses – meaning the user can easily see them, and IDEs should autocomplete them
  - (For v3 WebSockets only: `contract`, `unified_margin`, `spot`)


## [3.0.0rc0] - 2022-12-28
This version upgrades pybit to Bybit's version 3 (v3) APIs. Some old API modules are maintained due to lack of or only partial support in v3. Method names have been improved and conform to an intuitive standard.

Future modules will be removed as Bybit's APIs are further unified so that they may be accessible from just one or two modules which should generally be divided by account type (eg, unified margin) rather than by market type (eg USDT perpetual).

This is a pre-release, as indicated by the `rc` (release candidate) in the version number. Future versions may have breaking changes. An imminent major version of the Bybit API will introduce major changes before these v3 APIs make it to the production version.

### Added
- Bybit's main v3 HTTP and WebSocket APIs:
  - `contract` – inverse perpetuals, inverse futures, USDT perpetuals, and USDC options
  - `unified_margin` – USDT perpetuals and USDC options

### Modified
- `spot` to use v3 HTTP API and WebSocket APIs
- `account_asset` to use v3 HTTP API

### Removed
- `usdt_perpetual` because it is now accessible via `contract` and `unified_margin`


## [2.4.1rc0] - 2022-10-07
### Modified
- `is_connected()` and the WebSocket reconnection logic. 


## [2.4.1] - 2022-10-07
- See below release candidates for further changes.

### Fixed
- Wrong endpoint path in `usdc_perpetual.py`
- Wrong endpoint path in `account_asset.py`


## [2.4.0rc1] - 2022-09-20
### Fixed
- USDC API's timestamp parameter


## [2.4.0rc0] - 2022-09-15
### Modified
- The way in which the WebSocket handles errors, improving general usage and debugging (tracebacks) as well as clearly defining under which errors should the WebSocket attempt reconnection.

### Fixed
- USDC API's timestamp parameter to avoid the occasional ret_msg: error sign!


## [2.4.0] - 2022-07-26
### Added
- `HTTP` methods for account asset's [universal transfer API](https://bybit-exchange.github.io/docs/account_asset/#t-enableuniversaltransfer)

### Fixed
- USDC API to use the user's set `recv_window`

### Modified
- Did some internal code reorganisation


## [2.3.1] - 2022-07-20
### Modified
- The `ping_interval` to 20 seconds to ensure WebSocket connection stability

## [2.3.0] - 2022-06-24
### Added
- `HTTP` methods for the spot API's [Leveraged Token](https://bybit-exchange.github.io/docs/spot/#t-ltinfos) and [Cross Margin](https://bybit-exchange.github.io/docs/spot/#t-crossmargintrading) endpoints
- `agentSource` parameter when sending requests to place spot orders, which uses the `referral_id` argument, so that affiliates can track orders


## [2.2.3] - 2022-06-22
- There was a packaging problem with the previous version. There are no changes compared with 2.2.2.


## [2.2.2] - 2022-06-22 [YANKED]
- See below release candidates for further changes. TLDR: Improved WebSocket stability and reconnection logic.

### Added
- `retries` argument so that users specify how many times the WebSocket tries to reconnect upon disconnection
  - The default is `10`. To retry forever, set it to `0`. pybit will wait 1 second between each retry.

### Modified
- Improved the logging around WebSocket disconnection


## [2.2.2rc2] - 2022-06-15
### Added
- WebSocket topic resubscription so that when a WebSocket connection is dropped and then reconnected it should resume pushing the same data as before. Essentially, completes the expected functionality of reconnecting to the WebSocket.

### Modified
- `is_connected()` function to work with modules that utilise >1 WebSocket connections


## [2.2.2rc1] - 2022-06-10
### Added
- `is_connected()` function to `WebSocket` class so that you can check if your WebSocket connection is alive

### Fixed
- Bug where, upon WebSocket disconnection, pybit rapidly tries to re-establish the connection, which results in being banned by the CDN for malicious activity

## [2.2.2rc0] - 2022-06-10
### Modified
- Improved HTTP error handling and logging to ease troubleshooting

## [2.2.1] - 2022-06-07
### Modified
- `usdt_perpetual` -> `get_risk_limit()` to not require authentication

### Fixed
- `usdt_perpetual` -> `add_reduce_margin()` to use the correct request method

## [2.2.0] - 2022-05-25
### Added
- USDC options `WebSocket` and `HTTP` classes
- Deposit/withdrawal endpoints to `account_asset` module

## [2.1.2] - 2022-05-05
### Fixed
- Initiating a WebSocket object without an `api_key` or `api_secret` for objects that create multiple WebSocket connections
- Error thrown when processing WebSocket orderbook

## [2.1.1] - 2022-04-30
### Added  
- USDC perpetual `WebSocket` and `HTTP` classes
- USDT perpetual `extended_user_trade_records()` method

### Modified
- Expose all WebSocket arguments to users (fixing the previous "wonky and unintuitive" implementation by simplifying the inheritance design)
- See below release candidates for details.

## [2.1.1rc0] - 2022-04-14
### Modified
- Added arg (`trace_logging`) to enable websocket-client's trace logging, which reveals extra debug information regarding the websocket connection, including the raw sent & received messages
  - Note: the code implementation is a little wonky and unintuitive, and will be refined as much as possible before the proper release - although the functionality will remain the same.

## [2.1.0] - 2022-04-08
### Fixed
- The processing of `instrument_info` WebSocket messages so that the user receive a `"type": "snapshot"` every time, rather than having to do their own delta/snapshot processing 
- Fix `AttributeError: '_FuturesWebSocketManager' object has no attribute 'endpoint'` when attempting reconnect


## [2.0.1] - 2022-03-17
### Added
- `record_request_time` arg to `HTTP` classes which, if true, returns the response dictionary in a tuple with the request elapsed time - as recorded by `requests`

### Changed
- `websocket_example.py` to demonstrate callbacks clearly
- the license to reflect the transition to bybit-exchange

### Fixed
- `JSONDecodeError` when trying to subscribe to a spot private WebSocket stream

## [2.0.0] - 2022-03-09
### Added
- New modules for each API as part of a restructuring effort: `inverse_perpetual.py`, `usdt_perpetual.py`, `spot.py`, and more
  - see the [README](https://github.com/bybit-exchange/pybit/blob/master/README.md) for how to import these new modules 
  - `HTTP` and `WebSocket` classes within each applicable module
  - These classes use inheritance to reflect the structure of the Bybit APIs - due to the division of endpoints along the lines of different market types
  - This means that different classes can share their common endpoints, such as `api_key_info()`, whilst keeping their distinctive endpoints like `get_active_order()` separate
  
### Changed
- `WebSocket` functionality to use callbacks instead of polling
  - This means that instead of polling `ws.fetch()` for your latest WebSocket messages, you can now simply define a function (`my_callback_function`), and pass this as an argument upon subscribing to your chosen topic
    - see the [example file](https://github.com/bybit-exchange/pybit/blob/master/examples/websocket_example.py) for more information
  - This also removes the need to remember topic names and JSON formats, as you now directly call a class method to subscribe
  - There is also a `custom_topic_stream` method which can be used if a new WebSocket topic has been released by Bybit, but it's not been added to `pybit` yet
- `HTTP` classes will now instantiate a new HTTP session for each API (Spot (`spot.HTTP`), Account Asset (`account_asset.HTTP`), etc)
  - this is due to the restructuring of `pybit` to use class inheritance
- Generally, the restructuring has allowed a great amount of segregation of the internal code to occur, which will allow for easier future development
  
### Removed
- The `WebSocket` class from the `__init__.py` file, which was imported like so: `from pybit import WebSocket`
  - This is because of the aforementioned functionality changes, which also have the potential to improve performance (as a core no longer needs to be occupied polling `ws.fetch()`)
- However, the `HTTP` class was not removed from `__init__.py` in an effort to provide a unified alternative
  - Despite this, we would recommend preferring the market-specific modules

## [1.3.6] - 2022-02-28
### Changed
- Added `query_trading_fee_rate()`

## [1.3.5] - 2022-01-12
### Changed
- `position_mode_switch()` to support USDT perp: `/private/linear/position/switch-mode`


## [1.3.4] - 2021-12-30
### Added
- `endpoint` arg to `get_active_order()`

### Fixed
- A WebSocket test case, by raising an exception instead of logging

## [1.3.3] - 2021-12-24
- Improve `get_risk_limit()`
  - Fixed: call this endpoint without authentication
  - Supported `endpoint` argument for `my_position()`, allowing the user to call this method without supplying a symbol
    - `symbol` is not a required parameter for these endpoints, but pybit typically relies on it for deciding which endpoint to call

## [1.3.2] - 2021-11-05
- Enabled WebSocket `fetch()` to handle multiple position sides from linear perp symbols
- Fixed `fetch()` for private spot WebSocket
- Supported `endpoint` argument for `my_position()`, allowing the user to call this method without supplying a symbol
  - `symbol` is not a required parameter for these endpoints, but pybit typically relies on it for deciding which endpoint to call
- See below release candidates for details.

## [1.3.2rc2] - 2021-11-03
### Modified
- Alter the spot endpoint paths used for `get_active_order()` and `query_active_order()`

## [1.3.2rc1] - 2021-10-25
### Modified
- Fixed failure to load subscriptions when provided in as JSON strings

## [1.3.2rc0] - 2021-10-19
### Modified
- Fixed the spot auth WebSocket to ensure subscriptions are not required

## [1.3.1] - 2021-10-07
### Modified
- Fixed methods like `query_symbol()` (which have no API parameters) not working following the spot update

## [1.3.0] - 2021-09-24
### Added
- Implemented the Spot API in `HTTP`
- Implemented the Account Asset API in `HTTP`
- Implemented the Spot WebSocket in `WebSocket`

## [1.2.1] - 2021-07-15
### Removed
- Removed `position_mode_switch()` as the endpoint has not been released to mainnet yet

## [1.2.0] - 2021-07-09

### Added

- Added new `HTTP` methods for new endpoints
- Added new paths for existing methods

### Modified

- Fixed some old paths

### Deprecated

- `is_linear` argument in `get_risk_limit()`

## [1.1.19] - 2021-06-15

### Added

- Added some logic to decide if there is 'order_book' in order book snapshot push for WebSocket

## [1.1.18] - 2020-03-23

### Added

- Added `ignore_codes` argument to `HTTP` for status codes to not raise any errors on.

## [1.1.17] - 2020-03-21

### Modified

- Removed extra suffix definition block in `place_conditional_order`.
- Changed logger functionality so that it won't overwrite user's preferred logging settings.
- Fixed wrong number of arguments error inside WebSocket `on_message`, `on_close`, `on_open`, `on_error`.

## [1.1.16] - 2020-03-21

### Modified

- Fixed typo errors on endpoint urls.

## [1.1.15] - 2020-03-21

### Added

- Added support for futures endpoints on `HTTP` (using `isdigit` to detect futures symbols).

### Modified

- Using `get` method for `dict` for symbol check instead of calling by key.
- `endpoint` on `HTTP` will now default to https://api.bybit.com if no argument.
- `retry_codes` is now user-definable in the `HTTP` arguments.
- All logging is now on `DEBUG` level—user will need to manually set `logging_level` to `DEBUG`.
- Added attempted request to `FailedRequestError` and `InvalidRequestError` for improved error logging.

## [1.1.14] - 2020-02-06

### Modified

- Fixed unexpected `tuple` generation for status codes on `InvalidRequestError` and
  `FailedRequestError`.
- Fixed how `Websocket` handles incoming `orderBook` data due to Bybit's topic naming changes.

## [1.1.13] - 2020-02-01

### Modified

- `requests` will use `JSONDecodeError` from `simplejson` if it is available—`pybit` will now do the same to prevent
  errors.
- Fixed a bug where `HTTP` retry would crash on rate limit reached due to undefined variable.
- Improved `InvalidRequestError` and `FailedRequestError` to include error codes and times.

## [1.1.12] - 2020-01-20

### Modified

- `WebSocket` will now temporarily differentiate between inverse and linear endpoints for the 'order' topic
  since incoming data has differing keys.

## [1.1.11] - 2020-01-12

### Added

- `WebSocket` now has `purge_on_fetch` (defaults to `True`), which allows the user to keep data between fetches.

### Modified

- Fixed a bug on 'stop_order' for `WebSocket` that would prevent data from being appended due to deprecation 
  of `stop_order_id`.

## [1.1.10] - 2020-01-08

- See release candidates for details.

## [1.1.10rc0] - 2020-01-05

### Modified

- Rewrote if-condition on `_on_message` in `WebSocket` class to check for linear or non-linear position data.

## [1.1.9] - 2020-12-20

### Modified

- Added ability to handle `from` using `from_time` and `from_id` arguments since `from` is a
  reserved keyword.
- Removed `ignore_retries_for` from `HTTP`. `pybit` now uses a standard list of non-critical errors that can
  be retried.
- Added argument `retry_delay` for `HTTP`—allows user to add a custom retry delay for each retry.

## [1.1.8] - 2020-11-21

- See release candidates for details.

## [1.1.8rc4] - 2020-11-14

### Modified

- Fixed raise error missing argument for `FailedRequestError` upon max retries.
- Modified API endpoints to saistfy requirements for upcoming endpoint deprecation,
  see the [API Documentation](https://bybit-exchange.github.io/docs/inverse/#t-introduction)
  for more info.
- Updated `WebSocket` class to properly handle `candle` from USDT perpetual streams.
- Updated `WebSocket` class to return a copy of the collected data, preventing establishing
  a reference.
- Updated `WebSocket` class to properly handle linear (USDT) orderbook data.
- Performance improvements.

## [1.1.8rc3] - 2020-11-12

### Modified

- Changed `ignore_retries_for` default argument to be empty tuple to prevent error.

## [1.1.8rc2] - 2020-10-27

### Added

- Added `ignore_retries_for` argument to `HTTP` `auth` method, allowing the user
  to choose which error codes should NOT be retried.

## [1.1.8rc1] - 2020-10-27

### Added

- `FailedRequestError` and `InvalidRequestError` now have `message` and `status_code`
  attributes.

## [1.1.8rc0] - 2020-10-27

### Added

- Will now catch and handle `requests.exceptions.ConnectionError`.

## [1.1.7] - 2020-10-21

### Added

- Added `recv_window` error handler to `HTTP` `auth` method.
- Will now catch and handle `requests.exceptions.SSLError`.

## [1.1.6] - 2020-10-09

### Modified

- Added `recv_window` argument to `HTTP` class.

## [1.1.5] - 2020-09-30

### Modified

- Improved error handling.
- Added `max_retries` argument to `HTTP` class.

## [1.1.4] - 2020-09-17

### Modified

- Added `FailedRequestError` to differentiate between failed requests and
  invalid requests.
- Fixed `exit` method on `WebSocket` to now properly handle the closing of the socket.

## [1.1.3] - 2020-09-12

### Modified

- Increased expires time for WebSocket authentication to a full second.

## [1.1.2] - 2020-09-12

### Modified

- Add option to handle timeout on request submission.

## [1.1.1] - 2020-09-11

### Modified

- Fixed trailing decimal zero to prevent auth signature errors.

## [1.1.0] - 2020-09-08

### Added

- New `HTTP` methods.
- New argument for `HTTP` class to log each outgoing request.
- New argument for `WebSocket` class to attempt restart after an error is
  detected.

### Modified

- Mass simplification of all methods—each method now takes a series keyword
  arguments rather than a set number of required pre-defined arguments. This
  makes the library future-proof and prevents breaking on significant updates 
  to the REST API endpoints. This, however, requires the user to study the
  API documentation and know which arguments are required for each endpoint. 
- One new exception has been added—`InvalidRequestError`. This exception will be
  raised if Bybit returns with an error, or if `requests` is unable to complete
  the request.
- Inverse and Linear endpoints are now handled accordingly by differentiating
  from the symbol argument.
- Updated existing `HTTP` method names to follow the same naming procedure as 
  listed in the Bybit API documentation.
- Reformatting of code to follow PEP-8 standards.
- New docstring format.


## [1.0.2] - 2020-04-05

### Added

- Various logging features added to both HTTP and WebSocket classes.

### Modified

- Extensive WebSocket class updates.
  - Modified the WebSocketApp to send a heartbeat packet every 30 seconds,
    with a timeout of 10 seconds. These settings can be modified using the
    'ping_interval' and 'ping_timeout' arguments of the WebSocket
    constructor.
  - User no longer needs to manage the incoming stream; `pybit` does all the
  work (insert, update, delete).
  - Modified `ws.ping()` for ease of use; simply use the function to send
  heartbeat packets. When something happens to the connection, Python will
  raise an `Exception` which the end-user can catch and handle.
- Redundancy updates to the HTTP class.
- Modified the HTTP class to use an endpoint argument, allowing users to
  take advantage of the USDT endpoints.

## [1.0.1] - 2020-04-03

### Modified

- The setup.py file has been fixed to correctly install the pybit package.

## [1.0.0] - 2020-04-03

### Added

- The `pybit` module.
- MANIFEST, README, LICENSE, and CHANGELOG files.
