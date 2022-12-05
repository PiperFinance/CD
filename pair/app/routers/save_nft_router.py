import logging
from fastapi import APIRouter

from utils.nft.save_nfts import (
    save_user_all_nfts,
    save_user_chain_nfts
)
from utils.nft.save_nfts_nftbank import (
    save_user_all_nfts_nftbank,
    save_user_chain_nfts_nftbank
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
        save_user_all_nfts(request.userAddress)
        save_user_all_nfts_nftbank(request.userAddress)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_user_chain_nfts", response_model=BaseResponse)
async def save_single_user_chain_nfts(
    request: SaveUserChainData
):
    try:
        save_user_chain_nfts(
            request.chainId,
            request.userAddress
        )
        save_user_chain_nfts_nftbank(
            request.chainId,
            request.userAddress
        )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_nfts", response_model=BaseResponse)
async def save_multipule_users_nfts(
    request: SaveUsersData
):
    try:
        for address in request.userAddresses:
            save_user_all_nfts(address)
            save_user_all_nfts_nftbank(address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_chain_nfts", response_model=BaseResponse)
async def save_multipule_users_chain_nfts(
    request: SaveUsersChainData
):
    try:
        for address in request.userAddresses:
            save_user_chain_nfts(request.chainId, address)
            save_user_chain_nfts_nftbank(request.chainId, address)
        return BaseResponse()
    except Exception as e:
        logging.exception(e)
