import logging
from fastapi import APIRouter

from utils.pair.get_pairs import (
    get_all_pairs_len,
    get_all_pairs,
    get_chain_pairs_len,
    get_chain_pairs
)
from schemas.response_schema import PairList
from utils.types import ChainId


routes = APIRouter()


@routes.get("/get_pairs_len")
async def get_pairs_len() -> int:
    try:
        return get_all_pairs_len()
    except Exception as e:
        logging.exception(e)


@routes.get("/get_pairs", response_model=PairList)
async def get_pairs(
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        result = get_all_pairs(skip, page_size)
        return PairList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_chain_pairs_len")
async def get_single_chain_pairs_len(
    chain_id: ChainId
) -> int:
    try:
        result = get_chain_pairs_len(chain_id)
        return PairList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_chain_pairs", response_model=PairList)
async def get_single_chain_pairs(
    chain_id: ChainId,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        result = get_chain_pairs(
            chain_id,
            skip,
            page_size
        )
        return PairList(**{"result": result})
    except Exception as e:
        logging.exception(e)
