# Event API Completion Design

## Goal

Complete the Event Contract REST API exposed by `pybit.unified_trading.HTTP` by
adding the five endpoints present in the current Bybit V5 API documentation but
missing from the Event mixin.

## Public API

Add these methods and endpoint keys:

| HTTP method | Endpoint | SDK method | Event key | Auth |
| --- | --- | --- | --- | --- |
| GET | `/v5/event/instruments-info` | `get_ec_instruments_info` | `GET_EC_INSTRUMENTS_INFO` | No |
| GET | `/v5/event/orderbook` | `get_ec_orderbook` | `GET_EC_ORDERBOOK` | No |
| POST | `/v5/event/quotes` | `submit_ec_quote` | `SUBMIT_EC_QUOTE` | Yes |
| POST | `/v5/event/cancel` | `cancel_ec_quote` | `CANCEL_EC_QUOTE` | Yes |
| POST | `/v5/event/cancel-all` | `cancel_all_ec_quotes` | `CANCEL_ALL_EC_QUOTES` | Yes |

The method names retain the existing `ec` namespace used by the five Event
query methods and use verbs that distinguish reads from quote mutations.

## Implementation

- Extend `pybit.event.Event` with the five endpoint constants.
- Extend `pybit._v5_event.EventHTTP` with thin wrappers around
  `_submit_request`, following the existing Event methods.
- Pass keyword arguments through unchanged as `query=kwargs`.
- Do not add local request validation; parameter validation remains the API's
  responsibility, matching the rest of the SDK.
- No change is required in `unified_trading.HTTP` because it already inherits
  from `EventHTTP`.

## Documentation and Release Notes

Each method docstring will document required and optional request parameters
from the official endpoint page and link to that page. The `5.18.0` changelog
counts and lists will be increased from 53 to 58 methods and endpoint keys.

## Testing

Use test-driven development:

1. Add the five method/method/path/auth cases to the generated endpoint dispatch
   test and observe failures because the methods do not exist.
2. Add documentation URL assertions for all five methods.
3. Implement the Enum keys and HTTP wrappers, then run the focused test file.
4. Run the offline suite used by the publish workflow and `git diff --check`.

Success means all five methods are available on `unified_trading.HTTP`, dispatch
to the documented paths with the correct HTTP method and authentication flag,
and appear in the `5.18.0` changelog.
