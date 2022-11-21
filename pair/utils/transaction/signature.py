import requests
from typing import Dict, List

from configs.redis_config import cache_client, RedisNamespace


def cache_all_signatures():
    url = "https://www.4byte.directory/api/v1/signatures/"

    res = res.json()
    count = res.get("count")
    res = res.get("results")

    if count % 100 != 0:
        count = count // 100 + 2
    else:
        count = count // 100 + 1

    last_cached_page = cache_client().get(RedisNamespace.LAST_CACHED_SIG_PAGE)
    if last_cached_page == count - 1:
        return

    for i in range(count):
        cache_signatures(url, i, i + 400)


def cache_signatures(url: str, start: int, end: int):
    last_page = cache_client().get(RedisNamespace.LAST_CACHED_SIG_PAGE)

    if int(last_page) > start:
        start = last_page

    elif start == 1:
        res = get_single_page_signatures(url)
        cache_single_page_signature(res.get("results"), 1)

    else:
        for i in range(start, end):
            res = get_single_page_signatures(url)
            cache_single_page_signature(res.json(), i)


def get_single_page_signatures(url: str):
    res = requests.get(url)
    return res.json()


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
    if not signature:
        url = f"https://www.4byte.directory/api/v1/signatures/?hex_signature={sig_hex}"
        res = requests.get(url)
        res = res.get("results")[0].get("text_signature")
        cache_client().set(f'{RedisNamespace.FUNC_SIGNATURE}:{sig_hex}', res)
        return res
