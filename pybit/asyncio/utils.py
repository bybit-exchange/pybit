import asyncio


def get_event_loop():
    """Return the running event loop, or create+set a new one if none is running.

    Prefer ``asyncio.get_running_loop()`` inside coroutines. This helper exists
    only for pre-``asyncio.run`` construction paths in tests.
    """
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
