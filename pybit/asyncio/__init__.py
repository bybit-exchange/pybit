"""Async pybit.

**Experimental** — the shape of ``AsyncHTTP`` and ``AsyncWebsocketClient`` may
change in the next minor release. Pin the version if you need stability.

Basic usage::

    from pybit.asyncio.unified_trading import AsyncHTTP

    async with AsyncHTTP(testnet=True, api_key="...", api_secret="...") as client:
        result = await client.get_orderbook(category="linear", symbol="BTCUSDT")

The async surface requires two extra dependencies that are **not** installed
by ``pip install pybit`` — install them with the ``async`` extra::

    pip install "pybit[async]"

If they're missing at import time this module raises ``ImportError`` with the
hint above rather than a cryptic ``ModuleNotFoundError`` deep inside the
package.
"""

_MISSING_ASYNC_DEPS_HINT = (
    "pybit.asyncio requires optional dependencies that aren't installed. "
    "Install them with: pip install \"pybit[async]\"  "
    "(this adds aiohttp>=3.10.11,<4 and websockets>=12,<16 without affecting "
    "sync-only users)."
)


def _check_async_deps() -> None:
    """Verify aiohttp + websockets are importable.

    Called at ``pybit.asyncio`` import so callers see a single actionable
    error instead of a ``ModuleNotFoundError: No module named 'aiohttp'``
    surfacing from an internal file three imports deep.
    """
    missing = []
    try:
        import aiohttp  # noqa: F401
    except ImportError:
        missing.append("aiohttp")
    try:
        import websockets  # noqa: F401
    except ImportError:
        missing.append("websockets")
    if missing:
        raise ImportError(
            f"{_MISSING_ASYNC_DEPS_HINT} Missing: {', '.join(missing)}."
        )


_check_async_deps()
