import time
import logging
from typing import List
from utils.types import Price, Decimal, Contract


def get_reserves(pair_contract: Contract) -> List[int]:
    try:
        time.sleep(1)
        reserve0, reserve1, timestamp = pair_contract.functions.getReserves().call()
        return [reserve0, reserve1]
    except Exception as e:
        logging.exception(e)


def get_total_supply(pair_contract: Contract) -> int:
    try:
        time.sleep(1)
        total_supply = pair_contract.functions.totalSupply().call()
        return total_supply
    except Exception as e:
        logging.exception(e)


def calculate_lp_price(
        reserves: List[int],
        decimals: List[Decimal],
        prices: List[Price],
        total_supply: int) -> Price:
    
    try:
        lp_price = ((reserves[0] / decimals[0] * prices[0]) +
                    (reserves[1] / decimals[1] * prices[1])) / total_supply
        return lp_price
    except Exception as e:
        logging.exception(e)
        return 0
