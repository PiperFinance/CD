import requests
import logging
from pydantic import parse_obj_as
from typing import List, Dict
from web3 import Web3

from models import Chain, Nft, NftType
from utils.types import Address, ChainId
from utils.abis import nft_abi_721, nft_abi_1155


def save_user_all_nfts(address: Address):
    for chain_id in Chain.supported_chains():
        save_user_chain_nfts(chain_id, address)


def save_user_chain_nfts(
    chain_id: ChainId,
    address: Address
):
    for nft_type in NftType:
        nft_trxs = get_user_chain_nft_trxs(
            chain_id,
            address,
            nft_type.value
        )
        if nft_trxs in [None, []]:
            return
        users_nfts = find_to_trxs(address, nft_trxs)
        if users_nfts in [None, []]:
            return
        users_nfts = remove_from_trxs(address, nft_trxs, users_nfts)
        if users_nfts in [None, []]:
            return
        users_nfts = create_nfts(
            chain_id,
            address,
            users_nfts,
            nft_type.value
        )
        insert_nfts(chain_id, users_nfts)


def create_nfts(
    chain_id: ChainId,
    address: Address,
    users_nfts: Dict,
    nft_type: int
) -> List[Nft]:
    nfts = []
    for key, value in users_nfts.items():
        value["userAddress"] = Web3.toChecksumAddress(address)
        value["chainId"] = chain_id
        value["address"] = Web3.toChecksumAddress(key)
        value["type"] = nft_type
        value["idAddress"] = f'{value.get("address")}_{value.get("id")}'
        uri = get_nft_uri(
            NftType(nft_type),
            chain_id,
            value.get("address"),
            value.get("id")
        )
        if uri:
            value["uri"] = uri
        
        nft = parse_obj_as(Nft, value)
        nfts.append(nft.dict())
    return nfts


def get_nft_uri(
    nft_type: NftType,
    chain_id: ChainId,
    address: Address,
    id: str
):
    try:
        chain = Chain(chainId=chain_id)
        if nft_type is NftType.ERC721.value:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_721
            )
            return nft_contract.functions.tokenURI(int(id)).call()
        if nft_type == 1155:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_1155
            )
            return nft_contract.functions.uri(int(id)).call()

    except Exception as e:
        logging.exception(e)


def get_user_chain_nft_trxs(
    chain_id: ChainId,
    address: Address,
    nft_type: NftType
) -> List:

    chain = Chain(chainId=chain_id)
    url = chain.url

    if nft_type == 721:
        url = f"{url}?module=account&action=tokennfttx"
    if nft_type == 1155:
        url = f"{url}?module=account&action=token1155tx"

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
            url = f"{url}&apikey={api_key}"
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
                "id": str(trx.get("tokenID")),
                "name": trx.get("tokenName"),
                "symbol": trx.get("tokenSymbol"),
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
    nfts: List[Dict]
):
    client = Nft.mongo_client(chain_id)
    client.drop()

    for nft in nfts:
        try:
            client.insert_one(nft)

        except Exception as e:
            logging.exception(e)
            continue
