import requests
import json
import os


def _vai_tokens(via_token_list="https://github.com/viaprotocol/tokenlists/blob/main/tokenlists/all.json?raw=true"):
    chains = requests.get(via_token_list).json()
    _r = []
    for chain_tokens in chains.values():
        for token in chain_tokens:
            if token['chainId'] == '1666600000' or token['chainId'] == 1666600000:
                continue  # harmoni
            if int(token['chainId']) <= 0:
                continue  # solana or etc.
            if token['address'] == "FvwEAhmxKfeiG8SnEvq42hc6whRyY3EFYAvebMqDNDGCgxN5Z":
                continue  # coingecko
            if token['address'] == "0x":
                continue  # coingecko
            if not token['address']:
                continue  # clover ???

            _r.append(token)
    with open(os.path.join(os.getcwd(), "providers", "viaProtocol.json"), "w+") as f:
        json.dump({
            "name": "viaProtocol",
            "timestamp": "2022-04-06T22:19:09+00:00",
            "version": {
                "major": 1,
                "minor": 0,
                "patch": 0
            },
            "keywords": [
                "default"
            ],
            "tokens": _r
        }, f)
