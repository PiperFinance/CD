import json
import logging
from web3 import Web3
from typing import List, Dict, Tuple

from .lp_price import get_reserves, get_total_supply, calculate_lp_price
from .token_price import get_token_price
from models import Chain, Pair
from utils import abis


def save_all_pairs():
    for chain_id in Chain.supported_chains():
        save_chain_pairs(chain_id)


def save_chain_pairs(chain_id: int):
    factories = get_chain_factories(chain_id)
    if not factories:
        return
    tokens = get_chain_tokens(chain_id)
    if not tokens:
        return

    chain = Chain(chainId=chain_id)

    for factory in factories:
        chain_pairs = get_and_create_chain_pairs_objects(
            chain,
            factory.get("factory"),
            factory.get("name"),
            tokens
        )
        insert_pairs(chain_id, chain_pairs)


def save_chain_pairs_test(chain_id: int):
    factories = get_chain_factories(chain_id)
    if not factories:
        return
    tokens = get_chain_tokens(chain_id)
    if not tokens:
        return

    chain = Chain(chainId=chain_id)

    for factory in factories:
        chain_pairs = get_and_create_chain_pairs_objects_test(
            chain,
            factory.get("factory"),
            factory.get("name"),
            tokens
        )
        insert_pairs(chain_id, chain_pairs)


def get_chain_factories(chain_id: int) -> Dict:
    with open("utils/dexs.json") as f:
        factory_dict = json.load(f)

    for key in factory_dict:
        if key == str(chain_id):
            return factory_dict[key]


def get_chain_tokens(chain_id: int) -> Dict:
    with open("utils/tokens.json") as f:
        token_dict = json.load(f)

    for key in token_dict:
        if key == str(chain_id):
            return token_dict[key]


def get_and_create_chain_pairs_objects(
        chain: Chain,
        factory_address: str,
        dex_name: str,
        tokens: List[Dict]) -> List[Pair]:

    factory_contract = chain.w3.eth.contract(
        Web3.toChecksumAddress(factory_address),
        abi=abis.factory_abi)

    pairs = []

    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            token0 = Web3.toChecksumAddress(tokens[i].get("address"))
            token1 = Web3.toChecksumAddress(tokens[j].get("address"))
            pair = get_pair(factory_contract, token0, token1)
            if pair in [None, "0x0000000000000000000000000000000000000000"]:
                continue

            pair_contract = chain.w3.eth.contract(
                Web3.toChecksumAddress(pair), abi=abis.pair_abi)
            reserves = get_reserves(pair_contract)
            total_supply = get_total_supply(pair_contract)
            decimals = [
                tokens[i].get("decimals"),
                tokens[j].get("decimals")
            ]
            symbols = [
                tokens[i].get("symbol"),
                tokens[j].get("symbol")
            ]
            token_prices = [
                get_token_price(symbols[0]),
                get_token_price(symbols[1])
            ]

            decimals, token_prices, symbols = sort_pair_tokens(
                pair_contract, [token0, token1], decimals, token_prices, symbols)
            lp_price = calculate_lp_price(
                reserves, decimals, token_prices, total_supply)

            pair_obj = Pair(**{
                "chainId": chain.chainId,
                "address": pair,
                "name": f"{symbols[0]}-{symbols[1]}",
                "dex": dex_name,
                "decimals": decimals,
                "reserves": [str(reserve) for reserve in reserves],
                "totalSupply": str(total_supply),
                "price": lp_price
            })

            pairs.append(pair_obj)
    return pairs


def get_and_create_chain_pairs_objects_test(
        chain: Chain,
        factory_address: str,
        dex_name: str,
        tokens: List[Dict]) -> List[Pair]:

    pairs = []
    token_addresses = []
    for token in tokens:
        token_addresses.append(Web3.toChecksumAddress(token.get("address")))

    factory_contract = chain.w3.eth.contract(
        Web3.toChecksumAddress(factory_address),
        abi=abis.factory_abi)

    pairs_length = factory_contract.functions.allPairsLenght().call()

    for i in range(pairs_length):
        pair_address = factory_contract.functions.allPairs(i).call()
        pair_contract = chain.w3.eth.contract(pair_address, abi=abis.pair_abi)
        token0 = pair_contract.fucntions.token0().call()
        if token0 not in token_addresses:
            continue
        token1 = pair_contract.fucntions.token1().call()
        if token1 not in token_addresses:
            continue

        reserves = get_reserves(pair_contract)
        total_supply = get_total_supply(pair_contract)

        for token in tokens:
            if token0 == Web3.toChecksumAddress(token.get("address")):
                decimals0 = token.get("decimals")
                symbol0 = token.get("symbol")

            if token1 == Web3.toChecksumAddress(token.get("address")):
                decimals1 = token.get("decimals")
                symbol1 = token.get("symbol")

            if decimals0 and decimals1:
                break

        if None in [decimals0, decimals1]:
            continue

        token_prices = [
            get_token_price(symbol0),
            get_token_price(symbol1)
        ]

        lp_price = calculate_lp_price(
            reserves, [decimals0, decimals1], token_prices, total_supply)

        pair_obj = Pair(**{
            "chainId": chain.chainId,
            "address": pair_address,
            "name": f"{symbol0}-{symbol1}",
            "dex": dex_name,
            "decimals": [decimals0, decimals1],
            "reserves": [str(reserve) for reserve in reserves],
            "totalSupply": str(total_supply),
            "price": lp_price
        })
        pairs.append(pair_obj)
    return pairs


def insert_pairs(chain_id: int, pairs: List[Pair]):
    client = Pair.mongo_client(chain_id)
    try:
        client.delete_many()
    except Exception as e:
        logging.info(
            f"{str(e)} -> seems like there is no pair in mongo for {chain_id} chain.")
    client.insert_many(pairs)


def get_pair(
        factory_contract,
        token0: str,
        token1: str) -> str:
    pair = factory_contract.functions.getPair(token0, token1).call()
    return pair


def sort_pair_tokens(
        pair_contract,
        tokens: List[str],
        symbols: List[str],
        decimals: List[int],
        prices: List[float]) -> Tuple:

    token0 = pair_contract.functions.token0()
    if token0 == tokens[0]:
        return decimals, prices, symbols
    decimals = decimals.reverse()
    prices = prices.reverse()
    symbols = symbols.reverse()
    return decimals, prices, symbols
