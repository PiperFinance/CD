import requests
import logging
from web3 import Web3
from typing import List, Dict
from models import Trx, Chain
from .decode_transaction_input import decode_trx_input_data


def save_users_all_token_trxs(address: str):

    for chain_id in Chain.supported_chains():
        save_users_chain_token_trxs(chain_id, address)


def save_users_chain_token_trxs(chain_id: int, address: str):
    trxs = get_users_chain_token_trxs(
        chain_id,
        address
    )
    if trxs in [None, []]:
        return
    trxs = create_trx_objects(
        chain_id,
        address,
        trxs
    )
    insert_trxs(
        chain_id,
        trxs
    )


def get_users_chain_token_trxs(
    chain_id: int,
    address: str
) -> List[Dict]:

    chain = Chain(chainId=chain_id)
    url = chain.url
    api_keys = chain.api_keys

    data = {
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        # "page": 1,
        # "offset": 10,
        "sort": "asc",
    }

    for api_key in api_keys:
        try:
            url = f"{url}?module=account&action=tokentx&apikey={api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and (res.get("message") == "OK" or res.get("message") == "No transactions found"):
                return res.get("result")
        except Exception as e:
            logging.exception(f"{e} -> API Key didn't work.")
            continue


def create_trx_objects(chain_id: int, address: str, users_trxs: List[Dict]) -> List[Trx]:
    trxs = []

    for trx in users_trxs:
        trx["userAddress"] = Web3.toChecksumAddress(address)
        labels = decode_trx_input_data(trx.get("input"))
        if labels:
            trx["labels"] = labels
        trx["chainId"] = chain_id
        trx["fromAddress"] = trx.get("from")
        trxs.append(Trx(**trx))

    return trxs


def insert_trxs(chain_id: int, address: str, trxs: List[Trx]):
    client = Trx.mongo_client(chain_id)
    try:
        client.delete_many({"userAddress": address})
    except Exception as e:
        logging.info(
            f"{str(e)} -> seems like {address} on {chain_id} chain, doesn't have any trx in mongo yet.")
    client.insert_many(trxs)
