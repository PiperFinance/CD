import logging
import requests
from typing import Dict, List

from ..sync_redis import (
    cache_4bytes_signature,
    get_4bytes_signature_from_redis,
    cache_last_cached_signature_page,
    get_last_cached_signature_page_from_redis
)


def save_all_4bytes_signatures():
    url = "https://www.4byte.directory/api/v1/signatures/"

    res = requests.get(url).json()
    count = res.get("count")

    if count % 100 != 0:
        count = count // 100 + 2
    else:
        count = count // 100 + 1

    last_cached_page = get_last_cached_signature_page_from_redis()
    if last_cached_page == count - 1:
        return

    for i in range(0, count, 100):
        save_4bytes_signatures(url, i, i + 100)


def save_4bytes_signatures(url: str, start: int, end: int):
    last_cached_page = get_last_cached_signature_page_from_redis()

    if int(last_cached_page) > start:
        start = last_cached_page

    if start in [0, 1]:
        start = 2
        res = get_4bytes_single_page_signatures(page=0)
        if res not in [None, []]:
            save_4bytes_single_page_signature(res, 1)

    for i in range(start, end):
        res = get_4bytes_single_page_signatures(page=i)
        if res not in [None, []]:
            save_4bytes_single_page_signature(res, i)


def get_4bytes_single_page_signatures(page: int):
    url = "https://www.4byte.directory/api/v1/signatures/"

    if page >= 2:
        url = f"https://www.4byte.directory/api/v1/signatures/?={page}"
    try:
        res = requests.get(url=url)
        res = res.json()
        return res.get("results")
    except Exception as e:
        logging.exception(e)


def save_4bytes_single_page_signature(signatures: List[Dict], page_number: int):
    for signature in signatures:
        cache_4bytes_signature(signature.get("hex_signature"),
                               signature.get("text_signature"))
    cache_last_cached_signature_page(page_number)


def get_4bytes_single_signature(sig_hex: str) -> str:
    signature = get_4bytes_signature_from_redis(sig_hex)
    if signature:
        return signature

    url = f"https://www.4byte.directory/api/v1/signatures/?hex_signature={sig_hex}"
    signature = requests.get(url)
    signature = signature.json().get("results")
    if signature not in [[], None]:
        signature = signature[0].get("text_signature")
        cache_4bytes_signature(sig_hex, signature)
    return signature
