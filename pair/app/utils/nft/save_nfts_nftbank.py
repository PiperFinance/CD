import os
import requests
import logging
from web3 import Web3
from typing import List, Dict

from models import Chain, Nft
from utils.types import Address, ChainId, MongoClient
from utils.abis import nft_abi_721, nft_abi_1155
from .save_nfts import get_nft_uri

api_key = os.getenv("NFTBANK_APIKEY") or "b7e9b813bd7c0d8b06a23cd06833ffed"


def save_user_all_nfts_nftbank(
    user_address: Address
):
    nfts = []
    for chain_id in Chain.supported_chains():
        chain_nfts = save_user_chain_nfts_nftbank(
            chain_id,
            user_address
        )
        if chain_nfts not in [None, []]:
            nfts.extend(chain_nfts)
    return nfts


def save_user_chain_nfts_nftbank(
    chain_id: ChainId,
    user_address: Address
):
    base_url = "https://api.nftbank.ai/estimates-v2/user-inventory/"
    headers = {
        'x-api-key': api_key,
        "Content-Type": "application/json"
    }
    try:
        network_id = Chain(chainId=chain_id).chain_name
        url = f'{base_url}{network_id}/{user_address}'
        res = requests.get(url, headers=headers)
        res = res.json()
        if res.get("message") != "OK":
            return
        if res.get("data") in [None, []]:
            return
        nft_list = res.get("data")[0].get("asset_owned")
        if nft_list in [None, []]:
            return
        nfts = []
        for nft in nft_list:
            nfts.append({
                "address": Web3.toChecksumAddress(nft.get("asset_contract")),
                "id": nft.get("item_id").split("_")[1],
                "price": str(nft.get("floor_price_eth")),
                "type": nft.get("item_type").split("c")[1]
            })
        return nfts

    except Exception as e:
        logging.exception(e)


def insert_nftbank_nfts(
    chain_id: ChainId,
    nfts: List[Dict]
):
    client = Nft.mongo_client(chain_id)
    nfts = check_if_nftbank_nfts_exist(client, nfts)
    nfts = create_nftbank_nfts(nfts)
    client.insert_many(nfts)


def check_if_nftbank_nfts_exist(
    client: MongoClient,
    user_address: Address,
    nfts: List[Dict]
):
    user_nfts = list(client.find({"userAddress": user_address}))
    if user_nfts in [None, []]:
        return nfts

    nft_addresses_with_id = []

    for user_nft in user_nfts:
        nft_addresses_with_id.append(
            f"{user_nft.get('address')}_{user_nft.get('id')}")

    for nft in nfts:
        if f'{nft.get("address")}_{nft.get("id")}' in nft_addresses_with_id:
            query = {
                "userAddress": user_address,
                "address": nft.get("address")
            }
            newvalues = {"$set": {
                "price": nft.get("price"),
                "verified": True
            }}
            client.update_one(query, newvalues)
            nfts.remove(nft)
    return nfts


def create_nftbank_nfts(
    chain_id: ChainId,
    user_address: Address,
    nfts: List[Dict]
):
    nft_list = []
    for nft in nfts:
        try:
            nft_list.append(create_nftbank_nft(
                chain_id,
                user_address,
                nft.get("address"),
                nft.get("id"),
                nft.get("price"),
                nft.get("type")
            ))
        except Exception as e:
            logging.exception(e)


def create_nftbank_nft(
    chain_id: ChainId,
    user_address: Address,
    nft_address: Address,
    nft_id: str,
    price: str,
    nft_type: int
):
    nft = {
        "chainId": chain_id,
        "userAddress": user_address,
        "address": nft_address,
        "id": nft_id,
        "price": price,
        "verified": True
    }
    name = get_nft_name(
        nft_type,
        chain_id,
        nft_address
    )
    if name:
        nft["name"] = name
    symbol = get_nft_symbol(
        nft_type,
        chain_id,
        nft_address
    )
    if symbol:
        nft["symbol"] = symbol
    uri = get_nft_uri(
        nft_type,
        chain_id,
        nft_address,
        nft_id
    )
    if uri:
        nft["uri"] = uri
    return nft


def get_nft_name(
    nft_type: int,
    chain_id: ChainId,
    address: Address,
):
    try:
        chain = Chain(chainId=chain_id)
        if nft_type == 721:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_721
            )
        if nft_type == 1155:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_1155
            )
        return nft_contract.functions.name().call()

    except Exception as e:
        logging.exception(e)


def get_nft_symbol(
    nft_type: int,
    chain_id: ChainId,
    address: Address,
):
    try:
        chain = Chain(chainId=chain_id)
        if nft_type == 721:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_721
            )
        if nft_type == 1155:
            nft_contract = chain.w3.eth.contract(
                address,
                abi=nft_abi_1155
            )
        return nft_contract.functions.symbol().call()

    except Exception as e:
        logging.exception(e)
