import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

providers_tokens = {}
with open("providers.url.json") as f:
    providers = json.load(f)
for provider, url in providers.items():
    r = requests.get(url)
    if r.status_code == 200:
        try:
            res = r.json()
            if "tokens" in res.keys():
                with open(os.path.join("providers", provider + ".json"), "w+") as f:
                    json.dump(res, f)
                providers_tokens[provider] = res
        except json.JSONDecodeError:
            logger.error(f"Bad Request @ {provider} :  { r.text}")

"""Extra Info 
Zapper Swagger : https://api.zapper.fi/api/static/index.html
"""


"""Sample Obj {"address": "0x006BeA43Baa3f7A6f765F14f10A1a1b08334EF45", "chainId": 1, "name": "Stox", "symbol": "STX", "decimals": 18, "logoURI": "https://tokens.1inch.io/0x006bea43baa3f7a6f765f14f10a1a1b08334ef45.png"}"""
chain_seperated = {}
chain_seperated_and_merged_by_symbol = {}
chain_seperated_and_merged_by_name = {}

for provider, items in providers_tokens.items():
    for token in items["tokens"]:
        if (chainId := token["chainId"]) not in chain_seperated.keys():
            chain_seperated[chainId] = {}
            chain_seperated_and_merged_by_symbol[chainId] = {}
            chain_seperated_and_merged_by_name[chainId] = {}

        if (
            token_symbol := token["symbol"]
        ) not in chain_seperated_and_merged_by_symbol[chainId]:
            chain_seperated_and_merged_by_symbol[chainId][token_symbol] = []

        if (token_name := token["name"]) not in chain_seperated_and_merged_by_name[
            chainId
        ]:
            chain_seperated_and_merged_by_name[chainId][token_name] = []

        chain_seperated[chainId][token["address"]] = token
        chain_seperated_and_merged_by_name[chainId][token_name].append(token)
        chain_seperated_and_merged_by_symbol[chainId][token_symbol].append(token)

with open(os.path.join("out", "chain_seperated_and_merged_by_symbol.json"), "w+") as f:
    json.dump(chain_seperated_and_merged_by_symbol, f)

with open(os.path.join("out", "chain_seperated_and_merged_by_name.json"), "w+") as f:
    json.dump(chain_seperated_and_merged_by_name, f)

with open(os.path.join("out", "chain_seperated.json"), "w+") as f:
    json.dump(chain_seperated, f)
