import logging
from enum import Enum
from typing import Dict
import redis
from redis.client import Redis


global _CLIENT
global _CLIENT_BYTES
_CLIENT: Dict[int, Redis] = {}
_CLIENT_BYTES: Dict[int, Redis] = {}


class _Functions:

    def __add__(self, v) -> str:
        if isinstance(v, str):
            return str(self) + v
        raise ValueError

    def __str__(self) -> str:
        return self.value


class RedisNamespace(_Functions, Enum):
    COINGECK_COIN_ID = "cid:"
    LAST_CACHED_FUN_SELECTOR_PAGE = "lap:"
    FUNC_SELECTOR = "fus:"
    RPC_LIMIT = "rpc:"

    def __add__(self, v) -> str:
        if isinstance(v, str):
            return str(self) + v
        raise ValueError

    def __str__(self) -> str:
        return self.value

    def key(self, id: str) -> str:
        return f"{self.value}{id}"


async def initialize(url: str) -> bool:
    global _CLIENT
    global _CLIENT_BYTES

    _CLIENT[0] = redis.from_url(
        url=url, db=0, decode_responses=True)
    _CLIENT_BYTES[0] = redis.from_url(url=url, db=0)


def isConnected():
    cache_client().set("connection", "up")
    if cache_client().get("connection") == "up":
        return True
    print("REDIS IS NOT CONNECTED!")
    logging.critical("REDIS IS NOT CONNECTED!")
    return False


def cache_client() -> Redis:
    global _CLIENT
    return _CLIENT.get(0)


def cache_client_bytes() -> Redis:
    global _CLIENT_BYTES
    return _CLIENT_BYTES.get(0)
