import logging
from typing import List
from fastapi import APIRouter

from utils.transaction.save_transactions import (
    save_users_all_token_trxs,
    save_users_chain_token_trxs
)
from utils.types import Address, ChainId

routes = APIRouter()


@routes.post("/save_users_trxs")
async def save_users_trxs(user_address: Address):
    try:
        save_users_all_token_trxs(user_address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_users_chain_trxs")
async def save_users_chain_trxs(
    chain_id: ChainId,
    user_address: Address
):
    try:
        save_users_chain_token_trxs(chain_id, user_address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_trxs")
async def save_multipule_users_trxs(user_addresses: List[Address]):
    try:
        for address in user_addresses:
            save_users_all_token_trxs(address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_chain_trxs")
async def save_multipule_users_chain_trxs(
    chain_id: ChainId,
    user_addresses: List[Address]
):
    try:
        for address in user_addresses:
            save_users_chain_token_trxs(chain_id, address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)
