import logging
from typing import List
from fastapi import APIRouter

from utils.pair.get_pairs import (
    get_all_pairs_len,
    get_all_pairs,
    get_chain_pairs_len,
    get_chain_pairs
)
from models import Pair
from utils.types import ChainId

routes = APIRouter()


@routes.get("/get_pairs_len")
async def get_pairs_len() -> int:
    try:
        return get_all_pairs_len()
    except Exception as e:
        logging.exception(e)


@routes.get("/get_pairs", response_model=Pair)
async def get_pairs(
    page_size: int,
    page_number: int
) -> List[Pair]:
    try:
        skip = page_size * (page_number - 1)
        return get_all_pairs(skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_chain_pairs_len")
async def get_single_chain_pairs_len(chain_id: ChainId) -> int:
    try:
        return get_chain_pairs_len(chain_id)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_chain_pairs", response_model=Pair)
async def get_single_chain_pairs(
    chain_id: ChainId,
    page_size: int,
    page_number: int
) -> List[Pair]:
    try:
        skip = page_size * (page_number - 1)
        return get_chain_pairs(chain_id, skip, page_size)
    except Exception as e:
        logging.exception(e)
