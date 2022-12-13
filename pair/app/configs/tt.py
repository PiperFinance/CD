import json
import os
from pathlib import Path


p = Path(os.getcwd()).parent

with open(f"{p}/pair/app/utils/api_keys.json") as f:
    _api_keys = json.load(f)

api_keys = {}

for chain_id, api_key_list in _api_keys.items():
    api_keys[int(chain_id)] = api_key_list

with open(f"{p}/dexs/address_book.json") as f:
    _dexs = json.load(f)
    _dexs = _dexs.get("dexs")

dexs = {}

for chain_id, dex in _dexs.items():
    chain_dexs = []
    for chain_dex in dex.values():
        chain_dexs.append(chain_dex)
    dexs[int(chain_id)] = chain_dexs

a = "k"
