import logging
from typing import List, Dict

from models import FunctionSelector


def save_function_selectors(function_selectors: List[FunctionSelector]):
    function_selector_list = []
    for function_selector in function_selectors:
        function_selector_list.append(function_selector.dict())
    return insert_function_selectors(function_selector_list)


def insert_function_selectors(function_selectors: List[Dict]):
    try:
        client = FunctionSelector.mongo_client()
        client.insert_many(function_selectors)
    except Exception as e:
        logging.exception(e)


def save_function_selector(function_selector: FunctionSelector):
    try:
        function_selector = function_selector.dict()
        client = FunctionSelector.mongo_client()
        client.insert_one(function_selector)
    except Exception as e:
        logging.exception(e)
