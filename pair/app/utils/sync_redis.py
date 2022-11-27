import logging
import json

from models import Signature
from configs.redis_config import RedisNamespace, cache_client


def cache_coin_id(
    symbol: str,
    id: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.COINGECK_COIN_ID}{symbol}',
            id
        )
    except Exception as e:
        logging.exception(e)


def get_coin_id_from_redis(symbol: str):
    try:
        return cache_client().get(
            f'{RedisNamespace.COINGECK_COIN_ID}{symbol}'
        )
    except Exception as e:
        logging.exception(e)


def cache_4bytes_signature(
    hex_signature: str,
    text_signature: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.FOUR_BYTES_IGNATURE}{hex_signature}',
            text_signature
        )
    except Exception as e:
        logging.exception(e)


def get_4bytes_signature_from_redis(signature_hex: str):
    try:
        return cache_client().get(
            f'{RedisNamespace.FOUR_BYTES_IGNATURE}{signature_hex}')
    except Exception as e:
        logging.exception(e)


def cache_last_cached_signature_page(
    page_number: int
):
    cache_client().set(
        str(RedisNamespace.LAST_CACHED_SIG_PAGE),
        page_number
    )


def get_last_cached_signature_page_from_redis():
    try:
        return cache_client().get(str(RedisNamespace.LAST_CACHED_SIG_PAGE))
    except Exception as e:
        logging.exception(e)


def cache_func_sig_with_args(
    hex: str,
    signature: Signature
):
    try:
        signature = signature.dict()
        cache_client().set(
            f'{RedisNamespace.SIGNATURE}{hex}',
            json.dumps(signature)
        )
    except Exception as e:
        logging.exception(e)


def get_func_sig_with_args_from_redis(
    hex: str
) -> Signature:
    try:
        sig = cache_client().get(f'{RedisNamespace.SIGNATURE}{hex}')
        sig = json.loads(sig)
        return Signature(**sig)
    except Exception as e:
        logging.exception(e)
