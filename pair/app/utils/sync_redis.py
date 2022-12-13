import logging

from configs.redis_config import RedisNamespace, cache_client


def cache_coin_id(
    symbol: str,
    id: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.COINGECK_COIN_ID.value}{symbol}',
            id
        )
    except Exception as e:
        logging.exception(e)


def get_coin_id_from_redis(symbol: str):
    try:
        return cache_client().get(
            f'{RedisNamespace.COINGECK_COIN_ID.value}{symbol}'
        )
    except Exception as e:
        logging.exception(e)

