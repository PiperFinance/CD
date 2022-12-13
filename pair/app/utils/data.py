import requests
from pydantic import parse_raw_as, BaseModel
from utils.types import ChainId
from typing import List, Dict
from schemas import Token, Dex, Chain


class TokensChain(BaseModel):
    __root__: Dict[str, Token]


class DexsChain(BaseModel):
    __root__: Dict[str, Dex]


TOKENS:  TokensChain = parse_raw_as(
    TokensChain,
    requests.get(
        "https://github.com/PiperFinance/CD/blob/main/tokens/outVerified/chain_separated.json?raw=true").content
)


DEXS:  DexsChain = parse_raw_as(
    DexsChain,
    requests.get(
        "https://github.com/PiperFinance/CD/raw/main/dexs/address_book.json").content
)
DEXS = requests.get(
    "https://github.com/PiperFinance/CD/raw/main/dexs/address_book.json").json()
CHAINS = requests.get(
    "https://github.com/PiperFinance/CD/raw/main/chains/mainnet.json").json()


def get_tokens(chain_id: ChainId):
    return TOKENS.get(chain_id)
