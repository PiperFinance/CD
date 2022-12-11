import os
import uvicorn

from configs import redis_config, fastapi_config


DOMAIN = os.getenv("DOMAIN") or "http://localhost:12345" 
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6380"

app = fastapi_config.config(DOMAIN)


@app.on_event("startup")
async def app_boot():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()
    from test_functions import _tt_

    await _tt_()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12345)
