import uvicorn
from typing import List
from fastapi import FastAPI


from models import Trx, Pair, Nft
from configs.redis_config import initialize
from utils.nft.save_nfts import save_users_all_nfts
from utils.nft.get_nfts import get_users_all_nfts, get_users_chain_nfts
from utils.pair.get_pairs import get_all_pairs, get_chain_pairs
from utils.transaction.save_transactions import save_users_all_token_trxs
from utils.transaction.get_transactions import get_users_all_token_trxs, get_users_chain_token_trxs
from .test_functions import _tt_

REDIS_URL = "redis://localhost:6378"

app = FastAPI()


@app.on_event("startup")
async def app_boot():
    await initialize(REDIS_URL)
    await _tt_()


@app.post("/save_users_trxs")
async def save_users_trxs(user_address: str):
    save_users_all_token_trxs(user_address)
    return {"message": "success"}


@app.post("/save_multipule_users_trxs")
async def save_multipule_users_trxs(user_addresses: List[str]):
    for address in user_addresses:
        save_users_all_token_trxs(address)
    return {"message": "success"}


@app.get("/get_users_trxs", response_model=Trx)
async def get_users_trx_list(user_address: str):
    return get_users_all_token_trxs(user_address)


@app.get("/get_users_chain_trxs", response_model=Trx)
async def get_users_trx_list(chain_id: int, user_address: str):
    return get_users_chain_token_trxs(chain_id, user_address)


@app.post("/save_users_nfts")
async def save_users_nfts(user_address: str):
    save_users_all_nfts(user_address)
    return {"message": "success"}


@app.post("/save_multipule_users_nfts")
async def save_multipule_users_nfts(user_addresses: List[str]):
    for address in user_addresses:
        save_users_all_nfts(address)
    return {"message": "success"}


@app.get("/get_users_nfts", response_model=Nft)
async def get_users_nfts(user_address: str):
    return get_users_all_nfts(user_address)


@app.get("/get_users_chain_nfts", response_model=Nft)
async def get_users_nfts(chain_id: int, user_address: str):
    return get_users_chain_nfts(chain_id, user_address)


@app.get("/get_pairs", response_model=Pair)
async def get_pairs():
    return get_all_pairs()


@app.get("/get_chain_pairs", response_model=Pair)
async def get_pairs(chain_id: int):
    return get_chain_pairs(chain_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
