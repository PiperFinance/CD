import logging
from typing import List
from fastapi import APIRouter

from models import Nft
from utils.nft.get_nfts import (
    get_users_all_nfts_len,
    get_users_all_nfts,
    get_users_chain_nfts_len,
    get_users_chain_nfts
)
from utils.types import Address, ChainId

routes = APIRouter()


@routes.get("/get_users_nfts_len")
async def get_users_nfts(user_address: Address) -> int:
    try:
        return get_users_all_nfts_len(user_address)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_nfts", response_model=Nft)
async def get_users_nfts(
    user_address: Address,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        return get_users_all_nfts(user_address, skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_chain_nfts_len")
async def get_single_users_chain_nfts(
    chain_id: ChainId,
    user_address: Address
) -> int:
    try:
        return get_users_chain_nfts_len(chain_id, user_address)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_chain_nfts", response_model=Nft)
async def get_single_users_chain_nfts(
    chain_id: ChainId,
    user_address: Address,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        return get_users_chain_nfts(chain_id, user_address, skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_nfts_len")
async def get_multipule_users_nfts_len(
    user_addresses: List[Address]
) -> int:
    try:
        nft_len = 0
        for user_address in user_addresses:
            nft_len += get_users_all_nfts_len(user_address)
        return nft_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_nfts", response_model=Nft)
async def get_multipule_users_nfts(
    user_addresses: List[Address],
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        nfts = []
        for address in user_addresses:
            nfts.append(get_users_all_nfts(address, skip, page_size))
        return nfts
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_nfts_len")
async def get_single_users_chain_nfts(
    chain_id: ChainId,
    user_addresses: List[Address]
) -> int:
    try:
        nft_len = 0
        for user_address in user_addresses:
            nft_len += get_users_chain_nfts_len(chain_id, user_address)
        return nft_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_nfts", response_model=Nft)
async def get_multipule_users_chain_nfts(
    chain_id: ChainId,
    user_addresses: List[Address],
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        nfts = []
        for address in user_addresses:
            nfts.append(get_users_chain_nfts(
                chain_id, address, skip, page_size))
        return nfts
    except Exception as e:
        logging.exception(e)
