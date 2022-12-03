import logging

from configs.redis_config import RedisNamespace, cache_client
# from utils.types import ChainId


# def rpc_request(
#     chain_id: ChainId,
#     count=1
# ):
#     rpc_limit = 10 ** 10

#     key = f"{RedisNamespace.RPC_LIMIT.value}{chain_id}"
#     call_count = int(cache_client().get(key) or 0)
#     if call_count > rpc_limit:
#         return cache_client().ttl(key)
#     ex = 50 * 60
#     cache_client().set(key, call_count + count, ex=ex)
#     return 0


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


def cache_function_selector(
    hex_signature: str,
    text_signature: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.FUNC_SELECTOR.value}{hex_signature}',
            text_signature
        )
    except Exception as e:
        logging.exception(e)


def get_function_selector_from_redis(signature_hex: str):
    try:
        return cache_client().get(
            f'{RedisNamespace.FUNC_SELECTOR.value}{signature_hex}')
    except Exception as e:
        logging.exception(e)


def cache_last_cached_function_selector_page(
    page_number: int
):
    cache_client().set(
        str(RedisNamespace.LAST_CACHED_FUN_SELECTOR_PAGE.value),
        page_number
    )


def get_last_cached_function_selector_page_from_redis():
    try:
        return int(cache_client().get(str(RedisNamespace.LAST_CACHED_FUN_SELECTOR_PAGE.value)))
    except Exception as e:
        logging.exception(e)
