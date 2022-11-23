import logging
import requests
from typing import Dict, List

from configs.redis_config import cache_client, RedisNamespace


def cache_all_signatures():
    url = "https://www.4byte.directory/api/v1/signatures/"

    res = requests.get(url).json()
    count = res.get("count")

    if count % 100 != 0:
        count = count // 100 + 2
    else:
        count = count // 100 + 1

    last_cached_page = cache_client().get(RedisNamespace.LAST_CACHED_SIG_PAGE)
    if last_cached_page == count - 1:
        return

    for i in range(count):
        res.append(cache_signatures(url, i, i + 400))


def cache_signatures(url: str, start: int, end: int):
    last_page = cache_client().get(RedisNamespace.LAST_CACHED_SIG_PAGE)

    if int(last_page) > start:
        start = last_page

    if start in [0, 1]:
        start = 2
        res = get_single_page_signatures(url)
        if res not in [None, []]:
            cache_single_page_signature(res, 1)

    for i in range(start, end):
        new_url = f"https://www.4byte.directory/api/v1/signatures/?page={i}"
        res = get_single_page_signatures(new_url)
        if res not in [None, []]:
            cache_single_page_signature(res, i)


def get_single_page_signatures(url: str):
    try:
        res = requests.get(url)
        res = res.json()
        return res.get("results")
    except Exception as e:
        logging.exception(e)


def cache_single_page_signature(signatures: List[Dict], page_number: int):
    for signature in signatures:
        cache_client().set(
            f'{RedisNamespace.FUNC_SIGNATURE}:{signature.get("hex_signature")}',
            signature.get("text_signature")
        )
    cache_client().set(
        RedisNamespace.LAST_CACHED_SIG_PAGE,
        page_number
    )


def get_signature(sig_hex: str) -> str:
    signature = cache_client().get(
        f'{RedisNamespace.FUNC_SIGNATURE}:{sig_hex}')
    if signature:
        return signature

    url = f"https://www.4byte.directory/api/v1/signatures/?hex_signature={sig_hex}"
    signature = requests.get(url)
    signature = signature.json().get("results")
    if signature not in [[], None]:
        signature = signature[0].get("text_signature")
        cache_client().set(
            f'{RedisNamespace.FUNC_SIGNATURE}:{sig_hex}', signature)
    return signature
