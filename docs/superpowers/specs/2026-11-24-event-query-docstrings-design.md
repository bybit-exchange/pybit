# Event Query Docstrings Design

## Goal

Make the five authenticated Event query method docstrings fully describe the
request parameters currently published in the Bybit V5 API documentation.

## Documentation Changes

Update `pybit/_v5_event.py` without changing request behavior:

- `get_ec_order_history`: optional `symbol`, `orderId`, `orderLinkId`,
  `startTime`, `endTime`, `limit`, and `cursor`.
- `get_ec_active_orders`: optional `symbol`, `orderId`, `orderLinkId`, `limit`,
  and `cursor`.
- `get_ec_position_info`: optional `symbol`, `baseCoin`, `settleCoin`, `limit`,
  and `cursor`.
- `get_ec_settlements`: required `symbol`; optional `orderId`, `startTime`,
  `endTime`, `limit`, and `cursor`.
- `get_ec_trade_history`: required `symbol`; optional `orderId`, `orderLinkId`,
  `startTime`, `endTime`, `limit`, and `cursor`.

Descriptions will include documented defaults and ranges where applicable.
Parameter names and casing will match the wire API exactly.

## Testing

Add a table-driven pytest test in `tests/test_generated_openapi_endpoints.py`.
For each method, the table supplies the expected required and optional parameter
names. The test splits the docstring at `Optional args:` and asserts each name
appears in the correct section. Methods without required parameters must place
all documented parameters under `Optional args:`.

Use test-driven development: add the test first and confirm it fails against the
incomplete docstrings, update only the docstrings, then run the focused and
release-equivalent offline test suites.

## Non-goals

- No endpoint, HTTP method, authentication, or payload changes.
- No local parameter validation.
- No changelog entry because this corrects documentation for methods already
  listed in release 5.18.0.
