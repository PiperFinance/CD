import requests
import logging
from typing import List
from models import Trx, Chain


async def save_users_all_token_txs(address: str):
    trxs = []
    for chain_id in Chain.supported_chains():
        chain = Chain(chainId=chain_id)
        url = chain.url
        api_keys = chain.api_keys
        trxs.extend(await save_users_token_txs(
            chain_id,
            url,
            api_keys,
            address
        ))

    return trxs


async def save_users_token_txs(
    chain_id: int,
    url: str,
    api_keys: List[str],
    address: str
):

    data = {
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1000,
        "offset": 10,
        "sort": "asc",
    }

    for api_key in api_keys:
        trxs = []
        try:
            url = f"{url}?module=account&action=tokentx&apikey={api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and res.get("status") == "200" :
                for r in res.get("result"):
                    r["chainId"] = chain_id
                    r["fromAddress"] = r.get("from")
                    r = Trx(**r)
                    trxs.append(r)
                    await r.mongo_client.insert_one(r)
                    print(r)
                return trxs
                
        except Exception as e:
            logging.exception(f"{e} -> API Key didn't work.")
            continue

