import logging
from pycoingecko import CoinGeckoAPI
from functools import lru_cache

from ..sync_redis import cache_coin_id, get_coin_id_from_redis
from utils.types import Symbol, Price


def save_coins_id():
    cache_coin_id('FTM', 'fantom')

    cg = CoinGeckoAPI()
    coin_list = cg.get_coins_list()
    for coin in coin_list:
        cache_coin_id(coin.get("symbol"), coin.get("id"))


def get_coins_id(symbol: Symbol) -> str:
    id = get_coin_id_from_redis(symbol)

    if id:
        return id

    cg = CoinGeckoAPI()
    coin_list = cg.get_coins_list()
    for coin in coin_list:
        if symbol == coin.get("symbol").upper():
            return coin.get("id")


@lru_cache(10000)
def get_token_price(symbol: Symbol) -> Price:
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
