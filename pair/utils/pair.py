import logging
import json
from web3 import Web3
from pycoingecko import CoinGeckoAPI
from typing import List, Dict

from models import Chain, Pair
from utils import abis


async def save_all_pairs():
    pairs = []
    for chain_id in Chain.supported_chains():
        chain = Chain(chainId=chain_id)
        factories = find_chain_factories(chain_id)
        if not factories:
            continue
        tokens = find_chain_tokens(chain_id)
        if not tokens:
            continue

        for factory in factories:
            pairs.extend(await save_chain_pairs(
                chain,
                factory.get("factory"),
                factory.get("name"),
                tokens
            ))


def find_chain_factories(chain_id: int):
    with open("utils/dexs.json") as f:
        factory_dict = json.load(f)

    for key in factory_dict:
        if key == str(chain_id):
            return factory_dict[key]


def find_chain_tokens(chain_id: int):
    with open("utils/tokens.json") as f:
        token_dict = json.load(f)

    for key in token_dict:
        if key == str(chain_id):
            return token_dict[key]


async def save_chain_pairs(
        chain: Chain,
        factory_address: str,
        dex_name: str,
        tokens: List[Dict]):

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
            token_prices = [
                get_token_price(tokens[i].get("symbol")),
                get_token_price(tokens[j].get("symbol"))
            ]

            decimals, token_prices = sort_pair_tokens(
                pair_contract, [token0, token1], decimals, token_prices)
            lp_price = calculate_lp_price(
                reserves, decimals, token_prices, total_supply)

            pair_obj = Pair(**{
                "chainId": chain.chainId,
                "address": pair,
                "name": f"{tokens[i].get('symbol')}-{tokens[j].get('symbol')}",
                "dex": dex_name,
                "decimals": decimals,
                "reserves": [str(reserve) for reserve in reserves],
                "totalSupply": str(total_supply),
                "price": lp_price
            })

            await pair_obj.mongo_client.insert_one(pair_obj)
            pairs.append(pair_obj)
    return pairs


def get_pair(
        factory_contract,
        token0: str,
        token1: str):
    pair = factory_contract.functions.getPair(token0, token1).call()
    return pair


def get_reserves(pair_contract):
    reserve0, reserve1, timestamp = pair_contract.functions.getReserves().call()
    return [reserve0, reserve1]


def get_total_supply(pair_contract):
    total_supply = pair_contract.functions.totalSupply().call()
    return total_supply


def sort_pair_tokens(
        pair_contract,
        tokens: List[str],
        decimals: List[int],
        prices: List[float]):

    token0 = pair_contract.functions.token0()
    if token0 == tokens[0]:
        return decimals, prices
    decimals = decimals.reverse()
    prices = prices.reverse()
    return decimals, prices


def get_coins_id(symbol):
    cg = CoinGeckoAPI()
    coin_list = cg.get_coins_list()
    for coin in coin_list:
        if coin.get('symbol').upper() == symbol:
            # cache_client().set(TokenID + symbol,
            #                 coin.get('id'))
            return coin.get('id')


def get_token_price(symbol):
    cg = CoinGeckoAPI()
    try:
        cg = CoinGeckoAPI()
        token_id = get_coins_id(symbol)
        coin_price = cg.get_price(
            ids=token_id, vs_currencies='usd')
        price = coin_price.get(token_id).get('usd')
        return price

    except Exception as e:
        logging.warn(f'{str(e)} -> getting price of {symbol} failed')
        return 0


def calculate_lp_price(
        reserves: List[int],
        decimals: List[int],
        prices: List[float],
        total_supply: int):

    lp_price = ((reserves[0] / decimals[0] * prices[0]) +
                (reserves[1] / decimals[1] * prices[1])) / total_supply
    return lp_price
