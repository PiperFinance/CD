import logging
from fastapi import APIRouter

from utils.transaction.save_trxs import (
    save_user_all_token_trxs,
    save_user_chain_token_trxs
)
from schemas.request_schemas import (
    SaveUserData,
    SaveUserChainData,
    SaveUsersData,
    SaveUsersChainData
)
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_user_trxs", response_model=BaseResponse)
async def save_user_trxs(
    request: SaveUserData
):
    try:
        save_user_all_token_trxs(request.user_address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_user_chain_trxs", response_model=BaseResponse)
async def save_user_chain_trxs(
    request: SaveUserChainData
):
    try:
        save_user_chain_token_trxs(
            request.chainId,
            request.user_address
        )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_trxs", response_model=BaseResponse)
async def save_multipule_users_trxs(
    request: SaveUsersData
):
    try:
        for address in request.user_addresses:
            save_user_all_token_trxs(address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_chain_trxs", response_model=BaseResponse)
async def save_multipule_users_chain_trxs(
    request: SaveUsersChainData
):
    try:
        for address in request.user_addresses:
            save_user_chain_token_trxs(
                request.chainId,
                address
            )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)
