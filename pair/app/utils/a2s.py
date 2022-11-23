import asyncio

def async_run(func: asyncio.coroutine):
    loop = None
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    if loop is not None:
        return loop.run_until_complete(
            func
        )
    raise ValueError("Expected An Awaitable Object")
