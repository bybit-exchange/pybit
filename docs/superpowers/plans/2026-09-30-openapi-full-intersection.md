# Full OpenAPI–Docs Intersection Python SDK Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the 35 authenticated `/v5` GET/POST operations that exist in both the Bybit OpenAPI spec and public docs but are not represented in pybit `releaseSdk`.

**Architecture:** Add one enum/HTTP file pair per URL-level service prefix, then compose all ten new HTTP classes into `unified_trading.HTTP`. A table-driven no-network test verifies every generated method's verb, exact path, kwargs forwarding, and authentication; scanner-based verification proves backward compatibility and zero remaining `spec ∩ docs` gaps.

**Tech Stack:** Python 3.10+, `enum.Enum`, pybit `_V5HTTPManager`, pytest, Go source scanner, OpenAPI 3.1 YAML.

---

## File Structure

Create these focused enum/HTTP pairs:

- `pybit/crypto_loan_fixed.py`, `pybit/_v5_crypto_loan_fixed.py`
- `pybit/crypto_loan_flexible.py`, `pybit/_v5_crypto_loan_flexible.py`
- `pybit/dca.py`, `pybit/_v5_dca.py`
- `pybit/fcombobot.py`, `pybit/_v5_fcombobot.py`
- `pybit/fgridbot.py`, `pybit/_v5_fgridbot.py`
- `pybit/fht.py`, `pybit/_v5_fht.py`
- `pybit/fmartingalebot.py`, `pybit/_v5_fmartingalebot.py`
- `pybit/grid.py`, `pybit/_v5_grid.py`
- `pybit/rwa.py`, `pybit/_v5_rwa.py`
- `pybit/strategy.py`, `pybit/_v5_strategy.py`

Modify:

- `pybit/unified_trading.py:8` — import ten new HTTP classes.
- `pybit/unified_trading.py:47` — add ten HTTP bases.
- `CHANGELOG.md:8` — expand the existing uncommitted `5.17.1` entry from 1 to 36 methods/keys.

Test:

- `tests/test_generated_openapi_endpoints.py` — table-driven dispatch regression coverage for all 35 methods.

## Exact Generation Convention

Every enum file uses this exact structure, with the class and entries supplied in the task tables:

```python
from enum import Enum


class ServiceName(str, Enum):
    ENUM_KEY = "/v5/exact/spec/path"

    def __str__(self) -> str:
        return self.value
```

Every HTTP method uses this exact structure. `Required args:` is omitted only when the table has no required fields. All 35 methods have request parameters, so all signatures retain `**kwargs` and all calls include `query=kwargs` and `auth=True`.

```python
from ._http_manager import _V5HTTPManager
from .service_module import ServiceName


class ServiceNameHTTP(_V5HTTPManager):
    def method_name(self, **kwargs):
        """Operation summary.

        Required args:
            field (string): Field required by the OpenAPI operation.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/document-page
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{ServiceName.ENUM_KEY}",
            query=kwargs,
            auth=True,
        )
```

Descriptions must use the corresponding OpenAPI parameter description. If the spec description is empty, use the unambiguous sentence `<parameter name> required by this operation.` rather than inventing behavior.

### Task 1: Add the failing dispatch contract

**Files:**
- Create: `tests/test_generated_openapi_endpoints.py`

- [ ] **Step 1: Create the complete endpoint contract test**

```python
from unittest.mock import Mock

import pytest

from pybit.unified_trading import HTTP


CASES = [
    ("get_crypto_loan_fixed_available_inventory", "GET", "/v5/crypto-loan-fixed/available-inventory"),
    ("get_crypto_loan_flexible_available_inventory", "GET", "/v5/crypto-loan-flexible/available-inventory"),
    ("close_dca_bot", "POST", "/v5/dca/close-bot"),
    ("create_dca_bot", "POST", "/v5/dca/create-bot"),
    ("close_combo_bot", "POST", "/v5/fcombobot/close"),
    ("create_combo_bot", "POST", "/v5/fcombobot/create"),
    ("get_combo_detail", "POST", "/v5/fcombobot/detail"),
    ("get_combo_limit", "POST", "/v5/fcombobot/getlimit"),
    ("close_f_grid_bot", "POST", "/v5/fgridbot/close"),
    ("create_f_grid_bot", "POST", "/v5/fgridbot/create"),
    ("get_f_grid_detail", "POST", "/v5/fgridbot/detail"),
    ("validate_f_grid_input", "POST", "/v5/fgridbot/validate"),
    ("batch_create_tax_reports", "POST", "/v5/fht/compliance/tax/private/batch_create"),
    ("batch_query_tax_reports", "GET", "/v5/fht/compliance/tax/private/batch_query"),
    ("close_f_mart_bot", "POST", "/v5/fmartingalebot/close"),
    ("create_f_mart_bot", "POST", "/v5/fmartingalebot/create"),
    ("get_f_mart_detail", "POST", "/v5/fmartingalebot/detail"),
    ("get_f_mart_limit", "POST", "/v5/fmartingalebot/getlimit"),
    ("close_grid_bot", "POST", "/v5/grid/close-grid"),
    ("create_grid_bot", "POST", "/v5/grid/create-grid"),
    ("query_grid_detail", "POST", "/v5/grid/query-grid-detail"),
    ("validate_grid_input", "POST", "/v5/grid/validate-input"),
    ("get_convert_detail", "GET", "/v5/rwa/stocks/convert/detail"),
    ("get_convert_list", "GET", "/v5/rwa/stocks/convert/list"),
    ("submit_convert", "POST", "/v5/rwa/stocks/convert/submit"),
    ("get_multiplier_list", "GET", "/v5/rwa/stocks/market/getMultiplierList"),
    ("get_market_session", "GET", "/v5/rwa/stocks/market/session"),
    ("place_stocks_order", "POST", "/v5/rwa/stocks/order"),
    ("cancel_stocks_order", "POST", "/v5/rwa/stocks/order/cancel"),
    ("get_stocks_order_detail", "GET", "/v5/rwa/stocks/order/detail"),
    ("get_stocks_positions", "GET", "/v5/rwa/stocks/positions"),
    ("create_chase_order_strategy", "POST", "/v5/strategy/create"),
    ("query_strategy_list", "GET", "/v5/strategy/list"),
    ("query_strategy_order_list", "GET", "/v5/strategy/order-list"),
    ("stop_strategy", "POST", "/v5/strategy/stop"),
]


@pytest.mark.parametrize("name,method,path", CASES, ids=[case[0] for case in CASES])
def test_generated_endpoint_dispatch(name, method, path):
    client = HTTP.__new__(HTTP)
    client.endpoint = "https://api.bybit.com"
    client._submit_request = Mock(side_effect=lambda **kwargs: kwargs)

    result = getattr(client, name)(probe="value")

    assert result == {
        "method": method,
        "path": f"https://api.bybit.com{path}",
        "query": {"probe": "value"},
        "auth": True,
    }
```

- [ ] **Step 2: Run the contract test and verify RED**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m pytest -q tests/test_generated_openapi_endpoints.py -p no:cacheprovider`

Expected: 35 failures caused by missing attributes on `HTTP`; no syntax or import failure in pre-existing code.

### Task 2: Add fixed and flexible crypto-loan inventory services

**Files:**
- Create: `pybit/crypto_loan_fixed.py`
- Create: `pybit/_v5_crypto_loan_fixed.py`
- Create: `pybit/crypto_loan_flexible.py`
- Create: `pybit/_v5_crypto_loan_flexible.py`

- [ ] **Step 1: Create exact enum files**

```python
# pybit/crypto_loan_fixed.py
from enum import Enum


class CryptoLoanFixed(str, Enum):
    GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY = "/v5/crypto-loan-fixed/available-inventory"

    def __str__(self) -> str:
        return self.value
```

```python
# pybit/crypto_loan_flexible.py
from enum import Enum


class CryptoLoanFlexible(str, Enum):
    GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY = "/v5/crypto-loan-flexible/available-inventory"

    def __str__(self) -> str:
        return self.value
```

- [ ] **Step 2: Create HTTP classes using the exact generation convention**

| Module/class | Method | Verb | Enum key | Required args | Summary | Docs URL |
|---|---|---|---|---|---|---|
| `CryptoLoanFixedHTTP` | `get_crypto_loan_fixed_available_inventory` | GET | `GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY` | `currency (string)`, `term (string)`, `annualRate (string)` | Get fixed-term crypto-loan available inventory. | `https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/available-inventory` |
| `CryptoLoanFlexibleHTTP` | `get_crypto_loan_flexible_available_inventory` | GET | `GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY` | `currency (string)` | Get flexible crypto-loan available inventory. | `https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/available-inventory` |

Use imports `.crypto_loan_fixed import CryptoLoanFixed` and `.crypto_loan_flexible import CryptoLoanFlexible`, respectively. The two complete dispatch bodies are:

```python
return self._submit_request(
    method="GET",
    path=f"{self.endpoint}{CryptoLoanFixed.GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY}",
    query=kwargs,
    auth=True,
)
```

```python
return self._submit_request(
    method="GET",
    path=f"{self.endpoint}{CryptoLoanFlexible.GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY}",
    query=kwargs,
    auth=True,
)
```

- [ ] **Step 3: Compile the four files**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m py_compile pybit/crypto_loan_fixed.py pybit/_v5_crypto_loan_fixed.py pybit/crypto_loan_flexible.py pybit/_v5_crypto_loan_flexible.py`

Expected: exit 0.

- [ ] **Step 4: Commit the service pair**

```bash
git add pybit/crypto_loan_fixed.py pybit/_v5_crypto_loan_fixed.py pybit/crypto_loan_flexible.py pybit/_v5_crypto_loan_flexible.py
git commit -m "feat: add crypto loan inventory endpoints"
```

### Task 3: Add DCA, combo, futures-grid, martingale, and spot-grid services

**Files:**
- Create: `pybit/dca.py`, `pybit/_v5_dca.py`
- Create: `pybit/fcombobot.py`, `pybit/_v5_fcombobot.py`
- Create: `pybit/fgridbot.py`, `pybit/_v5_fgridbot.py`
- Create: `pybit/fmartingalebot.py`, `pybit/_v5_fmartingalebot.py`
- Create: `pybit/grid.py`, `pybit/_v5_grid.py`

- [ ] **Step 1: Create enum files with these exact class/member/path triples**

```text
DCA:
  CLOSE_DCA_BOT = "/v5/dca/close-bot"
  CREATE_DCA_BOT = "/v5/dca/create-bot"
FComboBot:
  CLOSE_COMBO_BOT = "/v5/fcombobot/close"
  CREATE_COMBO_BOT = "/v5/fcombobot/create"
  GET_COMBO_DETAIL = "/v5/fcombobot/detail"
  GET_COMBO_LIMIT = "/v5/fcombobot/getlimit"
FGridBot:
  CLOSE_F_GRID_BOT = "/v5/fgridbot/close"
  CREATE_F_GRID_BOT = "/v5/fgridbot/create"
  GET_F_GRID_DETAIL = "/v5/fgridbot/detail"
  VALIDATE_F_GRID_INPUT = "/v5/fgridbot/validate"
FMartingaleBot:
  CLOSE_F_MART_BOT = "/v5/fmartingalebot/close"
  CREATE_F_MART_BOT = "/v5/fmartingalebot/create"
  GET_F_MART_DETAIL = "/v5/fmartingalebot/detail"
  GET_F_MART_LIMIT = "/v5/fmartingalebot/getlimit"
Grid:
  CLOSE_GRID_BOT = "/v5/grid/close-grid"
  CREATE_GRID_BOT = "/v5/grid/create-grid"
  QUERY_GRID_DETAIL = "/v5/grid/query-grid-detail"
  VALIDATE_GRID_INPUT = "/v5/grid/validate-input"
```

Each file must include `from enum import Enum`, its listed class inheriting `(str, Enum)`, the listed members, and `__str__` exactly as defined in the generation convention.

- [ ] **Step 2: Create the five HTTP classes from this complete method manifest**

All methods are POST, signed, accept `**kwargs`, and use the docs URL `https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit`, the public page in which these endpoint paths occur.

| Class | Method / enum key | Required args |
|---|---|---|
| `DCAHTTP` | `close_dca_bot` / `CLOSE_DCA_BOT` | `bot_id (integer)`, `close_mode (integer)` |
| `DCAHTTP` | `create_dca_bot` / `CREATE_DCA_BOT` | `parameters (object)` |
| `FComboBotHTTP` | `close_combo_bot` / `CLOSE_COMBO_BOT` | `bot_id (integer)` |
| `FComboBotHTTP` | `create_combo_bot` / `CREATE_COMBO_BOT` | `leverage (string)`, `init_margin (string)`, `adjust_position_mode (integer)`, `symbol_settings (array)` |
| `FComboBotHTTP` | `get_combo_detail` / `GET_COMBO_DETAIL` | `bot_id (integer)` |
| `FComboBotHTTP` | `get_combo_limit` / `GET_COMBO_LIMIT` | `leverage (string)`, `init_margin (string)`, `adjust_position_mode (integer)`, `symbol_settings (array)` |
| `FGridBotHTTP` | `close_f_grid_bot` / `CLOSE_F_GRID_BOT` | `bot_id (integer)` |
| `FGridBotHTTP` | `create_f_grid_bot` / `CREATE_F_GRID_BOT` | `symbol (string)`, `grid_mode (integer)`, `min_price (string)`, `max_price (string)`, `cell_number (integer)`, `leverage (string)`, `grid_type (integer)`, `total_investment (string)` |
| `FGridBotHTTP` | `get_f_grid_detail` / `GET_F_GRID_DETAIL` | `bot_id (integer)` |
| `FGridBotHTTP` | `validate_f_grid_input` / `VALIDATE_F_GRID_INPUT` | `symbol (string)`, `cell_number (integer)`, `min_price (string)`, `max_price (string)`, `leverage (string)`, `grid_type (integer)`, `grid_mode (integer)` |
| `FMartingaleBotHTTP` | `close_f_mart_bot` / `CLOSE_F_MART_BOT` | `bot_id (integer)` |
| `FMartingaleBotHTTP` | `create_f_mart_bot` / `CREATE_F_MART_BOT` | `symbol (string)`, `martingale_mode (string)`, `leverage (string)`, `price_float_percent (string)`, `add_position_percent (string)`, `add_position_num (integer)`, `init_margin (string)`, `round_tp_percent (string)` |
| `FMartingaleBotHTTP` | `get_f_mart_detail` / `GET_F_MART_DETAIL` | `bot_id (integer)` |
| `FMartingaleBotHTTP` | `get_f_mart_limit` / `GET_F_MART_LIMIT` | `symbol (string)`, `martingale_mode (string)`, `leverage (string)` |
| `GridHTTP` | `close_grid_bot` / `CLOSE_GRID_BOT` | `grid_id (integer)`, `close_mode (integer)` |
| `GridHTTP` | `create_grid_bot` / `CREATE_GRID_BOT` | `symbol (string)`, `max_price (string)`, `min_price (string)`, `total_investment (string)`, `cell_number (integer)` |
| `GridHTTP` | `query_grid_detail` / `QUERY_GRID_DETAIL` | `grid_id (integer)` |
| `GridHTTP` | `validate_grid_input` / `VALIDATE_GRID_INPUT` | `symbol (string)`, `cell_number (integer)`, `min_price (string)`, `max_price (string)`, `total_investment (string)` |

For every row, emit the exact body below with the row's class and enum key; no method may hard-code the path:

```python
return self._submit_request(
    method="POST",
    path=f"{self.endpoint}{DCA.CLOSE_DCA_BOT}",
    query=kwargs,
    auth=True,
)
```

- [ ] **Step 3: Compile all ten files**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m py_compile pybit/dca.py pybit/_v5_dca.py pybit/fcombobot.py pybit/_v5_fcombobot.py pybit/fgridbot.py pybit/_v5_fgridbot.py pybit/fmartingalebot.py pybit/_v5_fmartingalebot.py pybit/grid.py pybit/_v5_grid.py`

Expected: exit 0.

- [ ] **Step 4: Commit bot services**

```bash
git add pybit/dca.py pybit/_v5_dca.py pybit/fcombobot.py pybit/_v5_fcombobot.py pybit/fgridbot.py pybit/_v5_fgridbot.py pybit/fmartingalebot.py pybit/_v5_fmartingalebot.py pybit/grid.py pybit/_v5_grid.py
git commit -m "feat: add bot service endpoints"
```

### Task 4: Add FHT tax endpoints

**Files:**
- Create: `pybit/fht.py`
- Create: `pybit/_v5_fht.py`

- [ ] **Step 1: Create `FHT` enum**

```python
from enum import Enum


class FHT(str, Enum):
    BATCH_CREATE_TAX_REPORTS = "/v5/fht/compliance/tax/private/batch_create"
    BATCH_QUERY_TAX_REPORTS = "/v5/fht/compliance/tax/private/batch_query"

    def __str__(self) -> str:
        return self.value
```

- [ ] **Step 2: Create `FHTHTTP` with both exact operations**

| Method | Verb / enum key | Required args | Docs URL |
|---|---|---|---|
| `batch_create_tax_reports` | POST / `BATCH_CREATE_TAX_REPORTS` | `startTime (integer)`, `endTime (integer)`, `items (array)` | `https://bybit-exchange.github.io/docs/v5/tax/batch-create` |
| `batch_query_tax_reports` | GET / `BATCH_QUERY_TAX_REPORTS` | `batchId (string)` | `https://bybit-exchange.github.io/docs/v5/tax/batch-query` |

Both methods use `path=f"{self.endpoint}{FHT.<ENUM_KEY>}"`, `query=kwargs`, and `auth=True`.

- [ ] **Step 3: Compile and commit**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m py_compile pybit/fht.py pybit/_v5_fht.py`

Expected: exit 0.

```bash
git add pybit/fht.py pybit/_v5_fht.py
git commit -m "feat: add FHT tax endpoints"
```

### Task 5: Add RWA stocks endpoints

**Files:**
- Create: `pybit/rwa.py`
- Create: `pybit/_v5_rwa.py`

- [ ] **Step 1: Create exact `RWA` enum**

```python
from enum import Enum


class RWA(str, Enum):
    GET_CONVERT_DETAIL = "/v5/rwa/stocks/convert/detail"
    GET_CONVERT_LIST = "/v5/rwa/stocks/convert/list"
    SUBMIT_CONVERT = "/v5/rwa/stocks/convert/submit"
    GET_MULTIPLIER_LIST = "/v5/rwa/stocks/market/getMultiplierList"
    GET_MARKET_SESSION = "/v5/rwa/stocks/market/session"
    PLACE_STOCKS_ORDER = "/v5/rwa/stocks/order"
    CANCEL_STOCKS_ORDER = "/v5/rwa/stocks/order/cancel"
    GET_STOCKS_ORDER_DETAIL = "/v5/rwa/stocks/order/detail"
    GET_STOCKS_POSITIONS = "/v5/rwa/stocks/positions"

    def __str__(self) -> str:
        return self.value
```

- [ ] **Step 2: Create `RWAHTTP` from the complete operation manifest**

| Method | Verb / enum key | Required args | Docs URL |
|---|---|---|---|
| `get_convert_detail` | GET / `GET_CONVERT_DETAIL` | none | `/docs/v5/stocks/convert-detail` |
| `get_convert_list` | GET / `GET_CONVERT_LIST` | none | `/docs/v5/stocks/convert-list` |
| `submit_convert` | POST / `SUBMIT_CONVERT` | `convertType (string)`, `symbol (string)`, `inputAmount (string)`, `frontMultiplier (string)`, `requestId (string)`, `flow (string)` | `/docs/v5/stocks/convert-submit` |
| `get_multiplier_list` | GET / `GET_MULTIPLIER_LIST` | `current (integer)`, `pageSize (integer)` | `/docs/v5/stocks/multiplier-list` |
| `get_market_session` | GET / `GET_MARKET_SESSION` | none | `/docs/v5/stocks/market-session` |
| `place_stocks_order` | POST / `PLACE_STOCKS_ORDER` | `symbol (string)`, `quoteToken (string)`, `side (string)`, `type (string)`, `timeInForce (string)`, `orderTime (integer)`, `requestId (string)` | `/docs/v5/stocks/place-order` |
| `cancel_stocks_order` | POST / `CANCEL_STOCKS_ORDER` | `orderNo (string)` | `/docs/v5/stocks/cancel-order` |
| `get_stocks_order_detail` | GET / `GET_STOCKS_ORDER_DETAIL` | none | `/docs/v5/stocks/order-detail` |
| `get_stocks_positions` | GET / `GET_STOCKS_POSITIONS` | none | `/docs/v5/stocks/positions` |

Expand every docs value to `https://bybit-exchange.github.io` plus the listed path. Every method uses `RWA.<ENUM_KEY>`, `query=kwargs`, and `auth=True`. Methods with no required fields still omit the `Required args:` section but retain `**kwargs` because optional parameters exist.

- [ ] **Step 3: Compile and commit**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m py_compile pybit/rwa.py pybit/_v5_rwa.py`

Expected: exit 0.

```bash
git add pybit/rwa.py pybit/_v5_rwa.py
git commit -m "feat: add RWA stocks endpoints"
```

### Task 6: Add strategy endpoints

**Files:**
- Create: `pybit/strategy.py`
- Create: `pybit/_v5_strategy.py`

- [ ] **Step 1: Create exact `Strategy` enum**

```python
from enum import Enum


class Strategy(str, Enum):
    CREATE_CHASE_ORDER_STRATEGY = "/v5/strategy/create"
    QUERY_STRATEGY_LIST = "/v5/strategy/list"
    QUERY_STRATEGY_ORDER_LIST = "/v5/strategy/order-list"
    STOP_STRATEGY = "/v5/strategy/stop"

    def __str__(self) -> str:
        return self.value
```

- [ ] **Step 2: Create `StrategyHTTP` from the exact operation manifest**

All docs links are `https://bybit-exchange.github.io/docs/v5/rate-limit/rate-limit`.

| Method | Verb / enum key | Required args |
|---|---|---|
| `create_chase_order_strategy` | POST / `CREATE_CHASE_ORDER_STRATEGY` | `category (string)`, `symbol (string)`, `side (string)`, `size (string)`, `strategyType (string)` |
| `query_strategy_list` | GET / `QUERY_STRATEGY_LIST` | none |
| `query_strategy_order_list` | GET / `QUERY_STRATEGY_ORDER_LIST` | `strategyId (string)` |
| `stop_strategy` | POST / `STOP_STRATEGY` | `strategyId (string)` |

Every method uses `Strategy.<ENUM_KEY>`, `query=kwargs`, and `auth=True`. `query_strategy_list` retains `**kwargs` because its request has optional filters.

- [ ] **Step 3: Compile and commit**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m py_compile pybit/strategy.py pybit/_v5_strategy.py`

Expected: exit 0.

```bash
git add pybit/strategy.py pybit/_v5_strategy.py
git commit -m "feat: add strategy endpoints"
```

### Task 7: Wire all services into unified trading

**Files:**
- Modify: `pybit/unified_trading.py:8-27`
- Modify: `pybit/unified_trading.py:47-68`

- [ ] **Step 1: Run the contract test before wiring and verify it is still RED**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m pytest -q tests/test_generated_openapi_endpoints.py -p no:cacheprovider`

Expected: failures because `HTTP` does not yet inherit the new service classes.

- [ ] **Step 2: Insert exact imports**

```python
from ._v5_crypto_loan_fixed import CryptoLoanFixedHTTP
from ._v5_crypto_loan_flexible import CryptoLoanFlexibleHTTP
from ._v5_dca import DCAHTTP
from ._v5_fcombobot import FComboBotHTTP
from ._v5_fgridbot import FGridBotHTTP
from ._v5_fht import FHTHTTP
from ._v5_fmartingalebot import FMartingaleBotHTTP
from ._v5_grid import GridHTTP
from ._v5_rwa import RWAHTTP
from ._v5_strategy import StrategyHTTP
```

Only insert lines; do not remove or reorder existing imports.

- [ ] **Step 3: Insert exact inheritance bases before the closing parenthesis**

```python
    CryptoLoanFixedHTTP,
    CryptoLoanFlexibleHTTP,
    DCAHTTP,
    FComboBotHTTP,
    FGridBotHTTP,
    FHTHTTP,
    FMartingaleBotHTTP,
    GridHTTP,
    RWAHTTP,
    StrategyHTTP,
```

Add a trailing comma to the existing final `SpreadHTTP` base before inserting, preserving all existing bases.

- [ ] **Step 4: Run the contract test and verify GREEN**

Run: `PYTHONPYCACHEPREFIX=/tmp/pybit-plan-pycache python3 -m pytest -q tests/test_generated_openapi_endpoints.py -p no:cacheprovider`

Expected: `35 passed`.

- [ ] **Step 5: Commit wiring and regression test**

```bash
git add pybit/unified_trading.py tests/test_generated_openapi_endpoints.py
git commit -m "feat: expose generated services through unified HTTP"
```

### Task 8: Consolidate the release note

**Files:**
- Modify: `CHANGELOG.md:8-16`
- Verify: `pybit/__init__.py:1`

- [ ] **Step 1: Confirm the existing uncommitted version remains 5.17.1**

Run: `python3 -c 'from pybit import VERSION; assert VERSION == "5.17.1"; print(VERSION)'`

Expected: `5.17.1`.

- [ ] **Step 2: Replace the current one-method release section**

Keep the heading `## 5.17.1 — unknown-date`. Change counts to `New Methods (36)` and `New Endpoint Keys (36)`. Preserve the existing market entries and append all method names and class-qualified enum keys from Tasks 2–6 in the same deterministic service/path order as the endpoint contract.

The complete method list must be:

```markdown
- get_option_base_coins
- get_crypto_loan_fixed_available_inventory
- get_crypto_loan_flexible_available_inventory
- close_dca_bot
- create_dca_bot
- close_combo_bot
- create_combo_bot
- get_combo_detail
- get_combo_limit
- close_f_grid_bot
- create_f_grid_bot
- get_f_grid_detail
- validate_f_grid_input
- batch_create_tax_reports
- batch_query_tax_reports
- close_f_mart_bot
- create_f_mart_bot
- get_f_mart_detail
- get_f_mart_limit
- close_grid_bot
- create_grid_bot
- query_grid_detail
- validate_grid_input
- get_convert_detail
- get_convert_list
- submit_convert
- get_multiplier_list
- get_market_session
- place_stocks_order
- cancel_stocks_order
- get_stocks_order_detail
- get_stocks_positions
- create_chase_order_strategy
- query_strategy_list
- query_strategy_order_list
- stop_strategy
```

The complete endpoint-key list must be:

```markdown
- Market.GET_OPTION_BASE_COINS
- CryptoLoanFixed.GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY
- CryptoLoanFlexible.GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY
- DCA.CLOSE_DCA_BOT
- DCA.CREATE_DCA_BOT
- FComboBot.CLOSE_COMBO_BOT
- FComboBot.CREATE_COMBO_BOT
- FComboBot.GET_COMBO_DETAIL
- FComboBot.GET_COMBO_LIMIT
- FGridBot.CLOSE_F_GRID_BOT
- FGridBot.CREATE_F_GRID_BOT
- FGridBot.GET_F_GRID_DETAIL
- FGridBot.VALIDATE_F_GRID_INPUT
- FHT.BATCH_CREATE_TAX_REPORTS
- FHT.BATCH_QUERY_TAX_REPORTS
- FMartingaleBot.CLOSE_F_MART_BOT
- FMartingaleBot.CREATE_F_MART_BOT
- FMartingaleBot.GET_F_MART_DETAIL
- FMartingaleBot.GET_F_MART_LIMIT
- Grid.CLOSE_GRID_BOT
- Grid.CREATE_GRID_BOT
- Grid.QUERY_GRID_DETAIL
- Grid.VALIDATE_GRID_INPUT
- RWA.GET_CONVERT_DETAIL
- RWA.GET_CONVERT_LIST
- RWA.SUBMIT_CONVERT
- RWA.GET_MULTIPLIER_LIST
- RWA.GET_MARKET_SESSION
- RWA.PLACE_STOCKS_ORDER
- RWA.CANCEL_STOCKS_ORDER
- RWA.GET_STOCKS_ORDER_DETAIL
- RWA.GET_STOCKS_POSITIONS
- Strategy.CREATE_CHASE_ORDER_STRATEGY
- Strategy.QUERY_STRATEGY_LIST
- Strategy.QUERY_STRATEGY_ORDER_LIST
- Strategy.STOP_STRATEGY
```

No second `5.17.1` heading and no `5.17.2` bump may be introduced.

- [ ] **Step 3: Commit release metadata**

```bash
git add CHANGELOG.md pybit/__init__.py
git commit -m "chore: prepare pybit 5.17.1 endpoint release"
```

### Task 9: Run full verification and coverage closure

**Files:**
- Verify: all created and modified files
- Artifacts: `/tmp/gen-sdk-python-artifacts/`

- [ ] **Step 1: Compile and import**

Run: `PYTHONPYCACHEPREFIX=/tmp/gen-sdk-python-final-pycache python3 -m compileall -q pybit`

Expected: exit 0.

Run: `python3 -B -c 'from pybit.unified_trading import HTTP; print("import-ok")'`

Expected: `import-ok`.

- [ ] **Step 2: Run endpoint dispatch coverage**

Run: `PYTHONPYCACHEPREFIX=/tmp/gen-sdk-python-test-pycache python3 -m pytest -q tests/test_generated_openapi_endpoints.py -p no:cacheprovider`

Expected: `35 passed`.

- [ ] **Step 3: Run the repository tests without the pre-existing live-network test**

Run: `PYTHONPYCACHEPREFIX=/tmp/gen-sdk-python-test-pycache python3 -m pytest -q -k 'not test_get_server_time_direct' -p no:cacheprovider`

Expected: all selected tests pass; exactly one live-network test is deselected.

- [ ] **Step 4: Run scanner backward-compatibility checks**

```bash
go run /Users/sh01591ml/bbu/bybit-sdk-skills/.claude/scripts/scan_funcs_python.go /Users/sh01591ml/bybit/pybit > /tmp/gen-sdk-python-scan-final.ndjson
```

Compare this scan to `/tmp/gen-sdk-python-scan-before.ndjson` by `(class, name)`. Expected:

- zero missing methods;
- zero missing enum entries;
- zero duplicate `(class, method name)` declarations;
- every newly added method has a non-empty resolved endpoint;
- method count increases by 35 beyond the post-market baseline;
- enum count increases by 35 beyond the post-market baseline.

- [ ] **Step 5: Recompute the spec/docs intersection**

Repeat the design's selection pipeline over the 315 max-depth-three YAML files, docs path set, and final scanner output. Deduplicate by normalized `(path, method)` and print every retained endpoint absent from the scanner.

Expected output:

```text
spec∩docs unique operations: 252
missing path+method: 0
```

- [ ] **Step 6: Check the final diff**

Run: `git diff --check`

Expected: no output, exit 0.

Run: `git status --short --branch`

Expected: `releaseSdk` with only the planned files and commits; no temporary generator or bytecode files.
