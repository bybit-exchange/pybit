# Full OpenAPI–Docs Intersection Python SDK Design

## Goal

Generate every currently missing Python SDK endpoint for which the endpoint's normalized path exists in both the Bybit OpenAPI specification and the public OpenAPI documentation. The target is the `releaseSdk` branch of `/Users/sh01591ml/bybit/pybit`.

## Baseline and Scope

The discovery snapshot contains 252 unique `(normalized path, HTTP method)` operations in `spec ∩ docs`. Of these, 217 are already represented by a pybit HTTP method. The remaining 35 operations are in scope.

The previously generated `GET /v5/market/option-base-coins` endpoint remains part of the same uncommitted release batch. After this design is implemented, the release batch will contain 36 new methods and 36 new enum keys in total.

Only REST `GET` and `POST` operations under `/v5` are in scope. WebSocket operations, non-`/v5` paths, response model generation, and paths present in only one source are out of scope.

## Selection Pipeline

1. Refresh the spec and docs repositories.
2. Parse OpenAPI YAML files using the workflow's existing maximum depth and extract direct `GET` and `POST` operations.
3. Normalize paths for comparison by lowercasing, treating `_` and `-` as equivalent, and removing trailing slashes. Preserve the original spec path for generated code.
4. Retain operations whose normalized path occurs in the docs path set.
5. Deduplicate by `(normalized path, HTTP method)`.
6. Exclude endpoints already resolved by the pybit source scanner.
7. Fail on raw-path collisions, method-name collisions, ambiguous authentication, or invalid operation metadata instead of silently dropping an endpoint.

## Module and Class Mapping

Each URL-level service prefix receives one enum module and one HTTP module.

| Prefix | Enum module/class | HTTP module/class | Methods |
|---|---|---|---:|
| `crypto_loan_fixed` | `crypto_loan_fixed.py` / `CryptoLoanFixed` | `_v5_crypto_loan_fixed.py` / `CryptoLoanFixedHTTP` | 1 |
| `crypto_loan_flexible` | `crypto_loan_flexible.py` / `CryptoLoanFlexible` | `_v5_crypto_loan_flexible.py` / `CryptoLoanFlexibleHTTP` | 1 |
| `dca` | `dca.py` / `DCA` | `_v5_dca.py` / `DCAHTTP` | 2 |
| `fcombobot` | `fcombobot.py` / `FComboBot` | `_v5_fcombobot.py` / `FComboBotHTTP` | 4 |
| `fgridbot` | `fgridbot.py` / `FGridBot` | `_v5_fgridbot.py` / `FGridBotHTTP` | 4 |
| `fht` | `fht.py` / `FHT` | `_v5_fht.py` / `FHTHTTP` | 2 |
| `fmartingalebot` | `fmartingalebot.py` / `FMartingaleBot` | `_v5_fmartingalebot.py` / `FMartingaleBotHTTP` | 4 |
| `grid` | `grid.py` / `Grid` | `_v5_grid.py` / `GridHTTP` | 4 |
| `rwa` | `rwa.py` / `RWA` | `_v5_rwa.py` / `RWAHTTP` | 9 |
| `strategy` | `strategy.py` / `Strategy` | `_v5_strategy.py` / `StrategyHTTP` | 4 |

All ten HTTP classes are imported by `pybit/unified_trading.py` and inserted into the `HTTP` multiple-inheritance list without modifying or removing existing bases.

## Endpoint Inventory

### Crypto loan

- `GET /v5/crypto-loan-fixed/available-inventory` → `get_crypto_loan_fixed_available_inventory`
- `GET /v5/crypto-loan-flexible/available-inventory` → `get_crypto_loan_flexible_available_inventory`

### Bot services

- `POST /v5/dca/close-bot` → `close_dca_bot`
- `POST /v5/dca/create-bot` → `create_dca_bot`
- `POST /v5/fcombobot/close` → `close_combo_bot`
- `POST /v5/fcombobot/create` → `create_combo_bot`
- `POST /v5/fcombobot/detail` → `get_combo_detail`
- `POST /v5/fcombobot/getlimit` → `get_combo_limit`
- `POST /v5/fgridbot/close` → `close_f_grid_bot`
- `POST /v5/fgridbot/create` → `create_f_grid_bot`
- `POST /v5/fgridbot/detail` → `get_f_grid_detail`
- `POST /v5/fgridbot/validate` → `validate_f_grid_input`
- `POST /v5/fmartingalebot/close` → `close_f_mart_bot`
- `POST /v5/fmartingalebot/create` → `create_f_mart_bot`
- `POST /v5/fmartingalebot/detail` → `get_f_mart_detail`
- `POST /v5/fmartingalebot/getlimit` → `get_f_mart_limit`
- `POST /v5/grid/close-grid` → `close_grid_bot`
- `POST /v5/grid/create-grid` → `create_grid_bot`
- `POST /v5/grid/query-grid-detail` → `query_grid_detail`
- `POST /v5/grid/validate-input` → `validate_grid_input`

### Tax/FHT

- `POST /v5/fht/compliance/tax/private/batch_create` → `batch_create_tax_reports`
- `GET /v5/fht/compliance/tax/private/batch_query` → `batch_query_tax_reports`

### RWA stocks

- `GET /v5/rwa/stocks/convert/detail` → `get_convert_detail`
- `GET /v5/rwa/stocks/convert/list` → `get_convert_list`
- `POST /v5/rwa/stocks/convert/submit` → `submit_convert`
- `GET /v5/rwa/stocks/market/getMultiplierList` → `get_multiplier_list`
- `GET /v5/rwa/stocks/market/session` → `get_market_session`
- `POST /v5/rwa/stocks/order` → `place_stocks_order`
- `POST /v5/rwa/stocks/order/cancel` → `cancel_stocks_order`
- `GET /v5/rwa/stocks/order/detail` → `get_stocks_order_detail`
- `GET /v5/rwa/stocks/positions` → `get_stocks_positions`

### Strategy

- `POST /v5/strategy/create` → `create_chase_order_strategy`
- `GET /v5/strategy/list` → `query_strategy_list`
- `GET /v5/strategy/order-list` → `query_strategy_order_list`
- `POST /v5/strategy/stop` → `stop_strategy`

## Generated API Pattern

Enum files contain one `str, Enum` class. Enum member names are the generated method names converted to upper snake case, and values are exact spec paths.

HTTP files contain one `_V5HTTPManager` subclass. Each method:

- uses `def method(self, **kwargs)` when the operation accepts any request parameter;
- documents required parameters from query/path parameters and request-body schemas;
- dispatches with the exact spec HTTP method and enum reference;
- passes `query=kwargs` for parameterized operations;
- adds `auth=True` only when the effective OpenAPI security requirement is non-empty;
- links to the matching public docs page.

All 35 planned operations are authenticated according to their effective OpenAPI security declaration. Existing source is preserved byte-for-byte except for the required insertions in `unified_trading.py`, the current release note, and the generated files.

## Release Handling

Keep the existing uncommitted version `5.17.1`. Update the current `5.17.1 — unknown-date` entry so it lists 36 new methods and 36 new endpoint keys, including `get_option_base_coins`. Do not add a second version bump or a second release section.

## Verification

Completion requires all of the following:

1. `python3 -m compileall -q pybit` succeeds with bytecode redirected outside the repository.
2. `from pybit.unified_trading import HTTP` succeeds.
3. A no-network dispatch test invokes every new method and verifies HTTP method, exact path, payload forwarding, and authentication flag.
4. The repository test suite passes, excluding only the existing live-network server-time test.
5. The before/after scanner reports no removed methods or enum members, no duplicate method definitions, and no dangling enum references.
6. A fresh `spec ∩ docs` comparison reports zero missing `(path, HTTP method)` operations within this design's `/v5` GET/POST scope.
7. `git diff --check` succeeds and the final diff contains no unrelated modifications.

## Failure Policy

Generation stops without release-note changes if parsing, mapping, authentication resolution, or baseline validation fails. Post-write verification failures are reported with the affected files and endpoints; generated changes are left visible for inspection and are not committed automatically.
