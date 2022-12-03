import logging
from fastapi import APIRouter
from typing import List

from models import FunctionSelector
from utils.transaction.save_function_selectors import (
    save_function_selectors,
    save_function_selector
)

routes = APIRouter()


@routes.post("/save_function_selectors")
async def save_func_selectors(function_selectors: List[FunctionSelector]):
    try:
        save_function_selectors(function_selectors)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_function_selector")
async def save_func_selector(function_selector: FunctionSelector):
    try:
        save_function_selector(function_selector)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)
