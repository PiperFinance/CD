import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from configs import redis_config, fastapi_config

load_dotenv()

PORT = int(os.getenv("PORT", 12345))
DOMAIN = os.getenv("DOMAIN") or "http://localhost"
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"

app = fastapi_config.config(DOMAIN, PORT)


@app.on_event("startup")
async def app_boot():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()
    from test_functions import _tt_

    await _tt_()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
