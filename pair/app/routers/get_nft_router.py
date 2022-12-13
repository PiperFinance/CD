import logging
from fastapi import APIRouter, Query
from typing import List

from utils.nft.get_nfts import (
    get_user_all_nfts_len,
    get_user_all_nfts,
    get_user_chain_nfts_len,
    get_user_chain_nfts
)
from schemas.response_schema import NftList
from utils.types import ChainId, Address

routes = APIRouter()


@routes.get("/get_user_nfts_len")
async def get_user_nfts_len(
    user_address: Address
) -> int:
    try:
        return get_user_all_nfts_len(user_address)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_user_nfts", response_model=NftList)
async def get_users_nfts(
    user_address: Address,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        result = get_user_all_nfts(
            user_address,
            skip,
            page_size
        )
        return NftList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_user_chain_nfts_len")
async def get_single_user_chain_nfts_len(
    chain_id: ChainId,
    user_address: Address
) -> int:
    try:
        return get_user_chain_nfts_len(
            chain_id,
            user_address
        )
    except Exception as e:
        logging.exception(e)


@routes.get("/get_user_chain_nfts", response_model=NftList)
async def get_single_user_chain_nfts(
    chain_id: ChainId,
    user_address: Address,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        result = get_user_chain_nfts(
            chain_id,
            user_address,
            skip,
            page_size
        )
        return NftList(**{"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_nfts_len")
async def get_multipule_users_nfts_len(
    user_addresses: List[Address] | None = Query(default=None)
) -> int:
    try:
        nft_len = 0
        for user_address in user_addresses:
            nft_len += get_user_all_nfts_len(user_address)
        return nft_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_nfts", response_model=NftList)
async def get_multipule_users_nfts(
    page_number: int,
    page_size: int,
    user_addresses: List[Address] | None = Query(default=None)
):
    try:
        skip = page_size * (page_number - 1)
        nfts = []
        for address in user_addresses:
            nfts.extend(get_user_all_nfts(address, skip, page_size))
        return NftList(**{"result": nfts})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_nfts_len")
async def get_multipule_users_chain_nfts_len(
    chain_id: ChainId,
    user_addresses: List[Address] | None = Query(default=None)
) -> int:
    try:
        nft_len = 0
        for user_address in user_addresses:
            nft_len += get_user_chain_nfts_len(chain_id, user_address)
        return nft_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_nfts", response_model=NftList)
async def get_multipule_users_chain_nfts(
    chain_id: ChainId,
    page_number: int,
    page_size: int,
    user_addresses: List[Address] | None = Query(default=None)
):

    try:
        skip = page_size * (page_number - 1)
        nfts = []
        for address in user_addresses:
            nfts.extend(get_user_chain_nfts(
                chain_id, address, skip, page_size))
        return NftList(**{"result": nfts})
    except Exception as e:
        logging.exception(e)
