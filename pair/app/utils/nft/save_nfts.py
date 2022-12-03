import requests
import logging
from typing import List, Dict
from web3 import Web3

from models import Chain, Nft
from utils.types import Address, ChainId, MongoClient
from utils.abis import nft_abi


def save_users_all_nfts(address: Address):
    for chain_id in Chain.supported_chains():
        save_users_chain_nfts(chain_id, address)


def save_users_chain_nfts(
    chain_id: ChainId,
    address: Address
):
    nft_trxs = get_users_chain_nft_trxs(chain_id, address)
    if nft_trxs in [None, []]:
        return
    users_nfts = find_to_trxs(address, nft_trxs)
    if users_nfts in [None, []]:
        return
    users_nfts = remove_from_trxs(address, nft_trxs, users_nfts)
    if users_nfts in [None, []]:
        return
    users_nfts = create_nfts(chain_id, address, users_nfts)
    insert_nfts(chain_id, address, users_nfts)


def create_nfts(
    chain_id: ChainId,
    address: Address,
    users_nfts: Dict
) -> List[Nft]:
    nfts = []
    for key, value in users_nfts.items():
        value["userAddress"] = Web3.toChecksumAddress(address)
        value["chainId"] = chain_id
        value["address"] = Web3.toChecksumAddress(key)
        try:
            chain = Chain(chainId=chain_id)
            nft_contract = chain.w3.eth.contract(
                value.get("address"),
                abi=nft_abi
            )
            id = value.get("id")
            uri = nft_contract.functions.tokenURI(int(id)).call()
            if uri:
                value["uri"] = uri
        except Exception as e:
            logging.exception(e)

        nfts.append(value)
    return nfts


def get_users_chain_nft_trxs(
    chain_id: ChainId,
    address: Address,
) -> List:

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
            url = f"{url}?module=account&action=tokennfttx&apikey={api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and (res.get("message") == "OK" or res.get("message") == "No transactions found"):
                return res.get("result")

        except Exception as e:
            logging.exception(f"{e} -> API Key didn't work.")
            continue


def find_to_trxs(
    address: Address,
    nft_trxs: List[Dict]
) -> Dict:
    users_nfts = {}
    for trx in nft_trxs:
        if Web3.toChecksumAddress(trx.get("to")) == Web3.toChecksumAddress(address):
            users_nfts[trx.get("contractAddress")] = {
                "id": trx.get("tokenID"),
                "name": trx.get("tokenName"),
                "symbol": trx.get("tokenSymbol"),
                "decimal": trx.get("tokenDecimal")
            }

    return users_nfts


def remove_from_trxs(
    address: Address,
    nft_trxs: List[Dict],
    users_nfts: Dict
) -> Dict:
    for trx in nft_trxs:
        if Web3.toChecksumAddress(trx.get("from")) == Web3.toChecksumAddress(address):
            if trx.get("contractAddress") in list(users_nfts.keys()):
                users_nfts.pop(trx.get("contractAddress"))

    return users_nfts


def insert_nfts(
    chain_id: ChainId,
    address: Address,
    nfts: List[Dict]
):
    try:
        client = Nft.mongo_client(chain_id)
        # client.drop()
        nfts = check_if_nft_exists(client, address, nfts)
        if nfts not in [None, []]:
            client.insert_many(nfts)

    except Exception as e:
        logging.info(
            f"{str(e)} -> seems like {address} on {chain_id} chain, doesn't have any nfts in mongo yet.")


def check_if_nft_exists(
    client: MongoClient,
    address: Address,
    nfts: List[Dict]
) -> List[Dict]:
    try:
        user_nfts = list(client.find({"userAddress": address}))

        if user_nfts in [None, []]:
            return nfts

        nft_addresses_with_id = []

        for user_nft in user_nfts:
            nft_addresses_with_id.append(
                f"{user_nft.get('address')}_{user_nft.get('id')}"
            )

        for nft in nfts:
            if f'{nft.get("address")}_{nft.get("id")}' in nft_addresses_with_id:
                nfts.remove(nft)
        return nfts
    except Exception as e:
        logging.exception(e)
        return nfts
