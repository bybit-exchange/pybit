# Generated API Docstrings Completion Design

## Goal

Complete request-parameter documentation for every new Alpha, Referral, and
SpotX method in release 5.18.0 without changing runtime request behavior.

## Source of Truth and Scope

Use the current English Bybit V5 documentation under these directories:

- `docs/v5/alpha`
- `docs/v5/referral`
- `docs/v5/finance/spot-x`

For every endpoint with request parameters, copy each top-level parameter's
exact wire name, required flag, type, defaults, ranges, and documented
dependencies into the matching SDK method docstring. Nested fields such as
`userIdList[].userId` and `tokenAddressInfo[].chainCode` are documented beneath
their parent parameter but are not treated as top-level keyword arguments.

Methods whose endpoint explicitly accepts no request parameters remain without
an args section. Existing accurate text may be retained; incomplete sections
will be expanded.

## Docstring Structure

- Required top-level parameters appear under `Required args:`.
- Optional top-level parameters appear under `Optional args:`.
- Parameter spelling and casing match the HTTP API exactly.
- Each entry uses `<name> (<type>): <description>`.
- Request dispatch, method signatures, endpoints, authentication, and return
  behavior remain unchanged.

## Regression Testing

Add a data-driven manifest to `tests/test_generated_openapi_endpoints.py` for
all Alpha, Referral, and SpotX methods whose official docs define parameters.
Each row records the method name plus required and optional top-level parameter
names. A shared assertion splits the method docstring into required and optional
sections and checks every parameter appears in the correct section.

The test is intentionally local and deterministic: it does not fetch official
documentation during CI. Updating the SDK against a future documentation
revision requires updating the manifest and docstring together.

## Verification

Follow TDD: add the complete manifest test and observe failures, update the
docstrings, then run the focused generated-endpoint tests and the
release-equivalent offline suite. Run `git diff --check` as the final formatting
gate.

## Non-goals

- Restoring or changing RWA APIs.
- Adding local parameter validation.
- Changing the 5.18.0 changelog, endpoint keys, or method list.
