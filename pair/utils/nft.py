import requests
import logging
from typing import List, Dict
from web3 import Web3

async def get_users_nft_txs(
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
        try:
            url = f"{url}?module=account&action=tokennfttx&apikey={api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and res.get("status") == "200":
                return res.get("result")

        except Exception as e:
            logging.exception(f"{e} -> API Key didn't work.")
            continue


async def find_users_nfts(
    address: str,
    nft_trxs: List[Dict]
):
    users_nfts = []
    for trx in nft_trxs:
        if Web3.toChecksumAddress(trx.get("to")) == Web3.toChecksumAddress(address):
            users_nfts.append()

