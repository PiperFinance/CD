import os
import uvicorn
from typing import List
from fastapi import FastAPI
# os.environ['PORT'] = "123654"


from models import Trx, Pair, Nft, Signature
from configs import redis_config
from utils.nft.save_nfts import save_users_all_nfts
from utils.nft.get_nfts import get_users_all_nfts, get_users_chain_nfts
from utils.pair.get_pairs import get_all_pairs, get_chain_pairs
from utils.transaction.save_transactions import save_users_all_token_trxs
from utils.transaction.get_transactions import get_users_all_token_trxs, get_users_chain_token_trxs
from utils.transaction.signature import save_signatures, get_signatures

from utils.types import Address, HexStr, ChainId


REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6380"

app = FastAPI()


@app.on_event("startup")
async def app_boot():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()
    from test_functions import _tt_

    # await _tt_()


@app.post("/save_func_selectors")
async def save_func_selectors(signatures: List[Signature]):
    save_signatures(signatures)
    return {"message": "success"}


@app.get("/get_func_selectors")
async def get_func_selectors(hexs: List[HexStr]):
    return get_signatures(hexs)


@app.post("/save_users_trxs")
async def save_users_trxs(user_address: Address):
    save_users_all_token_trxs(user_address)
    return {"message": "success"}


@app.post("/save_multipule_users_trxs")
async def save_multipule_users_trxs(user_addresses: List[Address]):
    for address in user_addresses:
        save_users_all_token_trxs(address)
    return {"message": "success"}


@app.get("/get_users_trxs", response_model=Trx)
async def get_users_trx_list(user_address: Address):
    return get_users_all_token_trxs(user_address)


@app.get("/get_users_chain_trxs", response_model=Trx)
async def get_users_trx_list(chain_id: int, user_address: str):
    return get_users_chain_token_trxs(chain_id, user_address)


@app.post("/save_users_nfts")
async def save_users_nfts(user_address: Address):
    save_users_all_nfts(user_address)
    return {"message": "success"}


@app.post("/save_multipule_users_nfts")
async def save_multipule_users_nfts(user_addresses: List[Address]):
    for address in user_addresses:
        save_users_all_nfts(address)
    return {"message": "success"}


@app.get("/get_users_nfts", response_model=Nft)
async def get_users_nfts(user_address: Address):
    return get_users_all_nfts(user_address)


@app.get("/get_users_chain_nfts", response_model=Nft)
async def get_users_nfts(chain_id: ChainId, user_address: Address):
    return get_users_chain_nfts(chain_id, user_address)


@app.get("/get_pairs", response_model=Pair)
async def get_pairs():
    return get_all_pairs()


@app.get("/get_chain_pairs", response_model=Pair)
async def get_pairs(chain_id: ChainId):
    return get_chain_pairs(chain_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12345)
