import logging
from typing import List
from fastapi import APIRouter

from models import FunctionSelector
from utils.transaction.get_function_selectors import (
    get_all_function_selectors,
    get_all_function_selectors_len,
    get_function_selectors,
    get_function_selector
)
from utils.types import HexStr

routes = APIRouter()


@routes.get("/get_all_function_selectors_len")
async def get_all_func_selectors_len() -> int:
    try:
        return get_all_function_selectors_len()
    except Exception as e:
        logging.exception(e)


@routes.get("/get_all_function_selectors", response_model=FunctionSelector)
async def get_all_func_selectors(
    page_size: int,
    page_number: int
) -> List[FunctionSelector]:
    try:
        skip = page_size * (page_number - 1)
        return get_all_function_selectors(skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_funcion_selectors", response_model=FunctionSelector)
async def get_func_selectors(
    hexs: List[HexStr]
) -> List[FunctionSelector]:
    try:
        return get_function_selectors(hexs)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_function_selector", response_model=FunctionSelector)
async def get_func_selectors(
    hex: HexStr
) -> FunctionSelector:
    try:
        return get_function_selector(hex)
    except Exception as e:
        logging.exception(e)