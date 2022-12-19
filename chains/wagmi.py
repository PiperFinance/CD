"""
Converts  https://chainid.network/chains.json chainList to Wagmi schema
Read more @ [wagmi-github](https://github.com/wagmi-dev/wagmi)
"""

import os
import sys
import json
import requests
from tqdm import tqdm
from web3 import Web3
from ast import literal_eval
from functools import lru_cache


chains = requests.get("https://chainid.network/chains.json").json()

all = []
main = []
test = []


def w3(rpc):
    w3 = Web3(Web3.HTTPProvider(rpc))
    if not w3.isConnected():
        print(f"RPCUrl {rpc} is not Working")
    return w3


def isContract(w3: Web3, address):  # multicall address
    return w3.eth.get_code(address).hex != '0x'


@lru_cache
def chain_w3(chainId: int):
    for chain in main:
        if chain.get('id') == chainId:
            if (rpc := chain.get("rpcUrls", {}).get("default", None)):
                return w3(rpc)


@lru_cache
def isContractChainId(address, chainId: int):
    if (w3 := chain_w3(chainId)):
        return isContract(w3, address)


def hasMultiCallV3(rpc):
    try:
        rpc = rpc.replace("${INFURA_API_KEY}",
                          "31d72a42f19f4a39a6d831f8b331f875")
        return isContract(w3(rpc), "0xcA11bde05977b3631167028862bE2a173976CA11")
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.flush()


for chain in tqdm(chains):
    if len(chain.get("rpc")) < 1:
        print(f"ChainId {chain.get('chainId')} has no rpc\n")
        continue

    o = {
        "nativeCurrency": chain.get("nativeCurrency"),
        "id": chain.get('chainId'),
        "name": chain.get('chain'),
        "network": chain.get('name')
    }

    if (rpcURLS := chain.get("rpc")):

        o["rpcUrls"] = {}
        #
        # ${ALCHEMY_API_KEY}

        for i, _rpc in enumerate(rpcURLS):
            rpc = _rpc.lower()
            if "wss://" in rpc or "ws://" in rpc:
                continue
            if "infura" in rpc:
                o["rpcUrls"]['infura'] = _rpc

            if "alchemy" in rpc:
                o["rpcUrls"]['alchemy'] = _rpc

            if "cloudflare" in rpc:
                o["rpcUrls"]['default'] = _rpc
                o["rpcUrls"]['public'] = _rpc
                break
            else:
                o["rpcUrls"]['default'] = _rpc
                o["rpcUrls"]['public'] = _rpc

    if 'default' not in o["rpcUrls"]:
        print(o)
        exit(0)

    if (ens := chain.get('ens')) is not None:
        o['ens'] = {"address": ens['registry']}

    if hasMultiCallV3(o["rpcUrls"]['default']):
        # FIXME - CHECK OTHER CHAINS ...
        o['multicall'] = {
            "address": "0xcA11bde05977b3631167028862bE2a173976CA11",
            "blockCreated":  0
        }

    if (explorers := chain.get('explorers')):
        o['blockExplorers'] = {
            "default": {
                "name": explorers[0].get('name'),
                "url": explorers[0].get('url')
            },
            "public": {
                "name": explorers[0].get('name'),
                "url": explorers[0].get('url')
            },
        }

    is_testnet = False
    for word in ["testnet", "test", "ropsten", "rinkby", "kovan", "test-net", "testy", "test net", "net-test"]:
        if word.lower() in str(chain).lower():
            is_testnet = True

            break
    o['testnet'] = is_testnet
    all.append(o)
    if is_testnet:
        test.append(o)
    else:
        main.append(o)

print(f"Main: {len(main)} ::: Test: {len(test)} ::: out: {len(all)} ")

with open(os.path.join("chains", "mainnet.json"), "w+") as f:
    json.dump(main, f)

with open(os.path.join("chains", "testnet.json"), "w+") as f:
    json.dump(test, f)

with open(os.path.join("chains", "allNets.json"), "w+") as f:
    json.dump(all, f)
