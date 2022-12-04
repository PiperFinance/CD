import logging
from typing import List
from fastapi import APIRouter

from models import Trx
from utils.transaction.get_transactions import (
    get_users_all_token_trxs_len,
    get_users_all_token_trxs,
    get_users_chain_token_trxs_len,
    get_users_chain_token_trxs
)
from utils.types import Address, ChainId

routes = APIRouter()


@routes.get("/get_users_trxs_len")
async def get_users_trxs_len(user_address: Address) -> int:
    try:
        return get_users_all_token_trxs_len(user_address)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_trxs", response_model=Trx)
async def get_users_trxs(
    user_address: Address,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        return get_users_all_token_trxs(user_address, skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_chain_trxs_len")
async def get_users_chain_trxs_len(
    chain_id: int,
    user_address: Address
) -> int:
    try:
        return get_users_chain_token_trxs_len(chain_id, user_address)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_chain_trxs", response_model=Trx)
async def get_users_chain_trxs(
    chain_id: int,
    user_address: str,
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)
        return get_users_chain_token_trxs(chain_id, user_address, skip, page_size)
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_trxs_len")
async def get_multipule_users_trxs_len(
    user_addresses: List[Address]
) -> int:
    try:
        trx_len = 0
        for user_address in user_addresses:
            trx_len += get_users_all_token_trxs_len(user_address)
        return trx_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_trxs", response_model=Trx)
async def get_multipule_users_trxs(
    user_addresses: List[Address],
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        trxs = []
        for address in user_addresses:
            trxs.append(get_users_all_token_trxs(address, skip, page_size))
        return trxs
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_trxs_len")
async def get_multipule_users_chain_trxs_len(
    chain_id: int,
    user_addresses: List[Address]
) -> int:
    try:
        trx_len = 0
        for user_address in user_addresses:
            trx_len += get_users_chain_token_trxs_len(chain_id, user_address)
        return trx_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_chain_trxs", response_model=Trx)
async def get_multipule_users_chain_trxs(
    chain_id: ChainId,
    user_addresses: List[Address],
    page_size: int,
    page_number: int
):
    try:
        skip = page_size * (page_number - 1)

        trxs = []
        for address in user_addresses:
            trxs.append(get_users_chain_token_trxs(
                chain_id, address, skip, page_size))
        return trxs
    except Exception as e:
        logging.exception(e)
