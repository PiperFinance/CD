import logging
import requests
from typing import Dict, List

from ..sync_redis import (
    cache_function_selector,
    get_function_selector_from_redis,
    cache_last_cached_function_selector_page,
    get_last_cached_function_selector_page_from_redis
)
from utils.types import HexStr


def save_all_4bytes_function_selectors():
    url = "https://www.4byte.directory/api/v1/signatures/"

    res = requests.get(url).json()
    count = res.get("count")

    if count % 100 != 0:
        count = count // 100 + 2
    else:
        count = count // 100 + 1

    last_cached_page = get_last_cached_function_selector_page_from_redis()
    if last_cached_page == count - 1:
        return

    for i in range(0, count, 100):
        save_4bytes_function_selectors(i, i + 100)


def save_4bytes_function_selectors(start: int, end: int):
    last_cached_page = get_last_cached_function_selector_page_from_redis()
    if last_cached_page:
        if last_cached_page > start:
            start = last_cached_page

    if start in [0, 1]:
        start = 2
        res = get_4bytes_single_page_function_selectors(page=0)
        if res not in [None, []]:
            save_4bytes_single_page_fucntion_selectors(res, 1)

    for i in range(start, end):
        res = get_4bytes_single_page_function_selectors(page=i)
        if res not in [None, []]:
            save_4bytes_single_page_fucntion_selectors(res, i)


def get_4bytes_single_page_function_selectors(page: int):
    url = "https://www.4byte.directory/api/v1/signatures/"

    if page >= 2:
        url = f"https://www.4byte.directory/api/v1/signatures/?={page}"
    try:
        res = requests.get(url=url)
        res = res.json()
        return res.get("results")
    except Exception as e:
        logging.exception(e)


def save_4bytes_single_page_fucntion_selectors(
    function_selectors: List[Dict],
    page_number: int
):
    for function_selector in function_selectors:
        text_signature = function_selector.get("text_signature")
        text_signature = text_signature.split("(", 1)
        text_signature = text_signature[0]

        cache_function_selector(
            function_selector.get("hex_signature"),
            text_signature)

    cache_last_cached_function_selector_page(page_number)


def get_4bytes_single_function_selector(hex: HexStr) -> str:
    fucntion_selector = get_function_selector_from_redis(hex)
    if fucntion_selector:
        return fucntion_selector

    url = f"https://www.4byte.directory/api/v1/signatures/?hex_signature={hex}"
    fucntion_selector = requests.get(url)
    fucntion_selector = fucntion_selector.json().get("results")
    if fucntion_selector not in [[], None]:
        fucntion_selector = fucntion_selector[0].get("text_signature")
        cache_function_selector(hex, fucntion_selector)
    return fucntion_selector
