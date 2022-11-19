import uvicorn
from fastapi import FastAPI


from models import Trx, Pair, Chain
from utils.transaction import save_users_all_token_txs
from utils.pair import save_all_pairs, save_chain_pairs, find_chain_tokens

app = FastAPI()


@app.on_event("startup")
async def app_boot():
    ...


@app.post("/save_trxs", response_model=Trx)
async def save_transaction(user_address: str):
    return await save_users_all_token_txs(user_address)


@app.get("/save_pairs", response_model=Pair)
async def save_pairs():
    # return await save_all_pairs()
    chain = Chain(**{"chainId":1})
    tokens = find_chain_tokens(1)
    return await save_chain_pairs(
        chain,
        "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "SushiSwap",
        tokens
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
