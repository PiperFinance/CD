import logging
from typing import List
from fastapi import APIRouter, Query

from models import FunctionSelector
from utils.transaction.get_function_selectors import (
    get_all_function_selectors,
    get_all_function_selectors_len,
    get_function_selectors,
    get_function_selector
)
from schemas.response_schema import (
    FunctionSelectorList,
    FunctionSelectorResponse
)
from utils.types import HexStr

routes = APIRouter()


@routes.get("/get_all_function_selectors_len")
async def get_all_func_selectors_len() -> int:
    try:
        return get_all_function_selectors_len()
    except Exception as e:
        logging.exception(e)


@routes.get(
    "/get_all_function_selectors",
    response_model=FunctionSelectorList
)
async def get_all_func_selectors(
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        result = get_all_function_selectors(skip, page_size)
        return FunctionSelectorList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get(
    "/get_funcion_selectors",
    response_model=FunctionSelectorList
)
async def get_func_selectors(
    hexs: List[HexStr] | None = Query(default=None)
):
    try:
        result = get_function_selectors(hexs)
        return FunctionSelectorList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get(
    "/get_function_selector",
    response_model=FunctionSelector
)
async def get_func_selectors(
    hex: HexStr
):
    try:
        result = get_function_selector(hex)
        return FunctionSelectorResponse(**{"result": result})
    except Exception as e:
        logging.exception(e)
