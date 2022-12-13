from fastapi import APIRouter


from . import (
    get_nfts,
    save_nfts
)

routers = APIRouter()


routers.include_router(
    save_nfts.routes,
    tags=["Save NFT"])

routers.include_router(
    get_nfts.routes,
    tags=["Get NFT"])

