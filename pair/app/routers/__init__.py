from fastapi import APIRouter


from . import (
    save_func_selector_router,
    get_func_selector_router,
    save_nft_router,
    get_nft_router,
    get_pair_router,
    save_trx_router,
    get_trx_router
)

routers = APIRouter()

routers.include_router(
    save_func_selector_router.routes,
    tags=["Save Function Selector"])

routers.include_router(
    get_func_selector_router.routes,
    tags=["Get Function Selector"])

routers.include_router(
    save_nft_router.routes,
    tags=["Save NFT"])

routers.include_router(
    get_nft_router.routes,
    tags=["Get NFT"])

routers.include_router(
    get_pair_router.routes,
    tags=["Get Pair"])


routers.include_router(
    save_trx_router.routes,
    tags=["Save Transaction"])

routers.include_router(
    get_trx_router.routes,
    tags=["Get Transaction"])
