import json
import os
from pathlib import Path
from pydantic import BaseConfig
from typing import Dict, List

from models import Chain
from utils.types import ChainId

p = Path(os.getcwd()).parent

with open(f'{p}/chains/mainnet.json') as f:
    _chains = json.load(f)

chains = {}

for chain in _chains:
    chains[chain.get("chainId")] = chain


with open(f"{p}/dexs/address_book.json") as f:
    _dexs = json.load(f)
    _dexs = _dexs.get("dexs")

dexs = {}

for chain_id, dex in _dexs.items():
    chain_dexs = []
    for chain_dex in dex.values():
        chain_dexs.append(chain_dex)
    dexs[int(chain_id)] = chain_dexs


with open(f"{p}/tokens/outVerified/all_tokens.json") as f:
    _tokens = json.load(f)

tokens = {}
chain_ids = Chain.supported_chains()

for chain_id in chain_ids:
    chain_tokens = []
    for token in _tokens:
        if token.get("chainId") == chain_id:
            chain_tokens.append(token)
    tokens[chain_id] = chain_tokens

with open(f"{p}/pair/app/utils/api_keys.json") as f:
    _api_keys = json.load(f)

api_keys = {}

for chain_id, api_key_list in _api_keys.items():
    api_keys[int(chain_id)] = api_key_list


class Constants(BaseConfig):
    chains: Dict[ChainId, Dict] = chains
    dexs: Dict[ChainId, List] = dexs
    tokens: Dict[ChainId, List] = tokens
    api_keys: Dict[ChainId, List]


constants = Constants()
