import requests
import logging
from web3 import Web3
from typing import List, Dict
from models import Trx, Chain
from .decode_transaction_input import decode_trx_input_data
from utils.types import Address, ChainId, MongoClient


def save_users_all_token_trxs(address: Address):

    for chain_id in Chain.supported_chains():
        save_users_chain_token_trxs(chain_id, address)


def save_users_chain_token_trxs(
    chain_id: ChainId,
    address: Address
):
    trxs = get_users_chain_token_trxs(
        chain_id,
        address
    )
    if trxs in [None, []]:
        return
    trxs = create_trxs(
        chain_id,
        address,
        trxs
    )
    insert_trxs(
        chain_id,
        address,
        trxs
    )


def get_users_chain_token_trxs(
    chain_id: ChainId,
    address: Address
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


def create_trxs(
        chain_id: ChainId,
        address: Address,
        users_trxs: List[Dict]
) -> List[Trx]:
    trxs = []

    for trx in users_trxs:
        trx["userAddress"] = Web3.toChecksumAddress(address)
        labels = decode_trx_input_data(trx.get("input"))
        if labels:
            trx["labels"] = labels
        trx["chainId"] = chain_id
        trx["fromAddress"] = trx.get("from")
        trx["timeStamp"] = int(trx.get("timeStamp"))
        trxs.append(trx)

    return trxs


def insert_trxs(
    chain_id: ChainId,
    address: Address,
    trxs: List[Trx]
):
    try:
        client = Trx.mongo_client(chain_id)
        # client.drop()
        trxs = check_if_trxs_exist(client, address, trxs)
        if trxs not in [None, []]:
            client.insert_many(trxs)
    except Exception as e:
        logging.exception(e)


def check_if_trxs_exist(
    client: MongoClient,
    address: Address,
    trxs: List[Dict]
):
    try:
        user_trxs = list(client.find({"userAddress": address}))

        if user_trxs in [None, []]:
            return trxs

        trx_hashes = []

        for user_trx in user_trxs:
            trx_hashes.append(user_trx.get("hash"))

        for trx in trxs:
            if trx.get("hash") in trx_hashes:
                trxs.remove(trx)
        return trxs
    except Exception as e:
        logging.exception(e)
        return trxs
