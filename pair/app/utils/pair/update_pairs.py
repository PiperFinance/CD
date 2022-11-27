from web3 import Web3


from models import Pair, Chain
from .lp_price import get_reserves, get_total_supply, calculate_lp_price
from .token_price import get_token_price
from utils import abis


def update_all_pairs():
    for chain_id in Chain.supported_chains():
        update_chain_pairs(chain_id)


def update_chain_pairs(chain_id: int):
    chain = Chain(chainId=chain_id)
    client = Pair.mongo_client(chain_id)
    pairs = client.find()
    for pair in pairs:
        symbols = pair.name.split('-')

        price0 = get_token_price(symbols[0])
        price1 = get_token_price(symbols[1])

        pair_contract = chain.w3.eth.contract(
            Web3.toChecksumAddress(pair.address), abi=abis.pair_abi)

        reverses = get_reserves(pair_contract)

        total_supply = get_total_supply(pair_contract)

        lp_price = calculate_lp_price(
            reverses,
            pair.deicmals,
            [price0, price1],
            total_supply

        )
        pair.reserves = reverses
        pair.totalSupply = total_supply
        pair.price = lp_price

