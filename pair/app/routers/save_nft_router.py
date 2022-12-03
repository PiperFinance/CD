import logging
from typing import List
from fastapi import APIRouter

from utils.nft.save_nfts import (
    save_users_all_nfts,
    save_users_chain_nfts
)
from utils.types import Address, ChainId

routes = APIRouter()


@routes.post("/save_users_nfts")
async def save_users_nfts(user_address: Address):
    try:
        save_users_all_nfts(user_address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_users_chain_nfts")
async def save_single_users_chain_nfts(
    chain_id: ChainId,
    user_address: Address
):
    try:
        save_users_chain_nfts(chain_id, user_address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_nfts")
async def save_multipule_users_nfts(user_addresses: List[Address]):
    try:
        for address in user_addresses:
            save_users_all_nfts(address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_chain_nfts")
async def save_multipule_users_chain_nfts(
    chain_id: ChainId,
    user_addresses: List[Address]
):
    try:
        for address in user_addresses:
            save_users_chain_nfts(chain_id, address)
        return {"message": "success"}
    except Exception as e:
        logging.exception(e)
