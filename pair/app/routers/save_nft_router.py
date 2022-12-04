import logging
from fastapi import APIRouter

from utils.nft.save_nfts import (
    save_user_all_nfts,
    save_user_chain_nfts
)
from schemas.request_schemas import (
    SaveUserData,
    SaveUserChainData,
    SaveUsersData,
    SaveUsersChainData
)
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_user_nfts", response_model=BaseResponse)
async def save_user_nfts(
    request: SaveUserData
):
    try:
        save_user_all_nfts(request.user_address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_user_chain_nfts", response_model=BaseResponse)
async def save_single_user_chain_nfts(
    request: SaveUserChainData
):
    try:
        save_user_chain_nfts(
            request.chain_id,
            request.user_address
        )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_nfts", response_model=BaseResponse)
async def save_multipule_users_nfts(
    request: SaveUsersData
):
    try:
        for address in request.user_addresses:
            save_user_all_nfts(address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_chain_nfts", response_model=BaseResponse)
async def save_multipule_users_chain_nfts(
    request: SaveUsersChainData
):
    try:
        for address in request.user_addresses:
            save_user_chain_nfts(request.chain_id, address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)
