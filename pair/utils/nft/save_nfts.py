import requests
import logging
from typing import List, Dict
from web3 import Web3

from models import Chain, Nft


def save_users_all_nfts(address: str):
    for chain_id in Chain.supported_chains():
        chain = Chain(chainId=chain_id)
        url = chain.url
        api_keys = chain.api_keys
        nft_trxs = get_users_chain_nft_trxs(address, url, api_keys)
        users_nfts = find_to_trxs(address, nft_trxs)
        users_nfts = remove_from_trxs(address, nft_trxs, users_nfts)
        users_nfts = create_nft_objects(chain_id, address, users_nfts)
        save_users_chain_nfts(chain_id, address, users_nfts)


def create_nft_objects(
    chain_id: int,
    address: str,
    users_nfts: Dict[Dict]
) -> List[Nft]:
    nfts = []
    for key, value in users_nfts.items():
        value["userAddress"] = Web3.toChecksumAddress(address)
        value["chainId"] = chain_id
        value["address"] = Web3.toChecksumAddress(key)
        nfts.append(Nft(**value))
    return nfts


def get_users_chain_nft_trxs(
    address: str,
    url: str,
    api_keys: List[str],
) -> List:

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


def find_to_trxs(
    address: str,
    nft_trxs: List[Dict]
) -> Dict:
    users_nfts = {}
    for trx in nft_trxs:
        if Web3.toChecksumAddress(trx.get("to")) == Web3.toChecksumAddress(address):
            users_nfts[trx.get("contractAddress")] = {
                "id": trx.get("tokenID"),
                "name": trx.get("tokenName"),
                "decimal": trx.get("tokenDecimal")
            }

    return users_nfts


def remove_from_trxs(
    address: str,
    nft_trxs: List[Dict],
    users_nfts: Dict[Dict]
) -> Dict:
    for trx in nft_trxs:
        if Web3.toChecksumAddress(trx.get("from")) == Web3.toChecksumAddress(address):
            if trx.get("contractAddress") in list(users_nfts.keys()):
                users_nfts.pop(trx.get("contractAddress"))

    return users_nfts


def save_users_chain_nfts(
    chain_id: int,
    address: str,
    nfts: List[Nft]
):
    client = Nft.mongo_client(chain_id)
    try:
        client.delete_many({"userAddress": address})
    except Exception as e:
        logging.info(f"{str(e)} -> seems like {address} on {chain_id} chain, doesn't have any nfts in mongo yet.")

    client.insert_many(nfts)
