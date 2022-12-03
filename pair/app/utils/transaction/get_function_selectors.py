from typing import List

from models import FunctionSelector
from utils.types import HexStr


def get_all_function_selectors(
    skip: int,
    limit: int
) -> List[FunctionSelector]:
    client = FunctionSelector.mongo_client()
    if skip < 1:
        function_selectors = list(client.find().limit(limit))
    else:
        function_selectors = list(client.find().skip(skip).limit(limit))

    if function_selectors in [None, []]:
        return
    function_selector_list = []

    for function_selector in function_selectors:
        function_selector_list.append(FunctionSelector(**function_selector))


def get_all_function_selectors_len():
    client = FunctionSelector.mongo_client()
    return len(list(client.find()))


def get_function_selectors(
    hexs: List[HexStr],
) -> List[FunctionSelector]:
    function_selectors = []

    for hex in hexs:
        client = FunctionSelector.mongo_client()
        function_selector = client.find_one({"hex": hex})
        if function_selector:
            function_selectors.append(FunctionSelector(**function_selector))

    return function_selectors


def get_function_selector(hex: HexStr) -> FunctionSelector:
    client = FunctionSelector.mongo_client()
    function_selector = client.find_one({"hex": hex})
    if function_selector:
        return FunctionSelector(**function_selector)
