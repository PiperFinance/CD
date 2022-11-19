from typing import Optional, Any
import glob
import json
import logging
import os
import pickle
import time
from pathlib import Path
from uuid import uuid4

import requests
from thefuzz import fuzz  # type:ignore
from tqdm import tqdm
from web3 import Web3  # type:ignore
from web3.exceptions import ContractLogicError

logger = logging.getLogger(__name__)

_cache = {}
_failed_chains = []


with open("token.abi") as f:
    TOKEN_ABI = json.load(f)

with open(os.path.join(Path(os.getcwd()).parent.absolute(), "chains", "chains.json")) as f:
    _file = json.load(f)
    _CHAINS = {int(c['chainId']): c for c in _file}
    _W3s = {int(_c['chainId']): Web3(Web3.HTTPProvider(_c['rpc'][0]))
            for _c in _file if _c.get('rpc')}

    _CONTRACTS = {}
    for wc in _file:
        if wc.get('rpc'):
            rpc = wc.get('rpc')[0]
            if "${INFURA_API_KEY}" in rpc:
                rpc = rpc.replace("${INFURA_API_KEY}",
                                  "31d72a42f19f4a39a6d831f8b331f875")
            w3 = Web3(Web3.HTTPProvider(rpc))

            def _(_address, _w3=w3):
                return _w3.eth.contract(_address, abi=TOKEN_ABI)
            _.__name__ = "F" + str(uuid4())
            _CONTRACTS[int(wc['chainId'])] = _


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


def fetch_tokens(out_dir="providers"):
    """Extra Info
    Zapper Swagger : https://api.zapper.fi/api/static/index.html
    """
    providers_tokens = {}
    with open("providers.url.json") as f:
        providers = json.load(f)
    for provider, url in tqdm(providers.items()):
        r = requests.get(url)
        if r.status_code == 200:
            try:
                res = r.json()
                if "tokens" in res.keys():
                    with open(os.path.join(out_dir, provider + ".json"), "w+") as f:
                        json.dump(res, f)
                    providers_tokens[provider] = res
            except json.JSONDecodeError:
                logger.error(f"Bad Request @ {provider} :  { r.text}")
    return providers_tokens


def get_fetched_providers(search_dir="providers"):
    r = {}
    for file in glob.glob(os.path.join(os.getcwd(), search_dir, "*.json")):
        with open(os.path.join(os.getcwd(), search_dir, file)) as f:
            r[file.replace(".json", "").split(
                "\\" if os.name == 'nt' else "/")[-1]] = json.load(f)
    return r


def _token_key(token: dict):
    return (token['address'], token['chainId'])


def check_token_symbol(token, provider: Optional[str] = None):
    if token['chainId'] in _failed_chains:
        return token
    try:

        old_symb = token['symbol']
        # Usage of cache
        if (token_key := _token_key(token)) not in _cache:
            _cache[token_key] = _CONTRACTS[token['chainId']](
                token['address']).functions.symbol().call()
        # Cache Old symbol
        if provider:
            token[provider + "_symbol"] = token['symbol']
        token['symbol'] = _cache[token_key]
        if old_symb != token['symbol']:
            print(f"  old:{old_symb}, new:{token['symbol']} \t {token}")
    except ContractLogicError as e:
        print(" ", token, e)
        return None
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        _failed_chains.append(token['chainId'])
        print("  ", _CONTRACTS[token['chainId']](
            token['address']).web3.provider, token['chainId'])
        return token
    except Exception as e:
        if "to C ssize_t" in str(e):
            return token
        else:
            print("  ",  token['address'],
                  token['chainId'], token['symbol'], e, type(e))
            return None

    return token


def check_token_address(token):
    _add = token['address']
    match _add:
        case "0xaa44051bdd76e251aab66dbbe82a97343b4d7da3#code":
            _add = '0xaa44051bdd76e251aab66dbbe82a97343b4d7da3'
        case "0x77F86D401e067365dD911271530B0c90DeC3e0f7/":
            _add = "0x77F86D401e067365dD911271530B0c90DeC3e0f7"
        case "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2#balances":
            _add = "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2"
    try:
        token['address'] = Web3.toChecksumAddress(_add)
    except Exception as e:
        print(" Bad Address", e, token)
        return None

    return token


def fix_fechted_providers(fetched_providers_data: dict):
    for provider, data in fetched_providers_data.items():
        _res_tokens = []
        _bad_tokens = []
        print(f"\nProvider: {provider}")
        for token in tqdm(data['tokens']):
            token = check_token_address(token)
            if token is not None:
                token = check_token_symbol(token)
            if token is not None:
                _res_tokens.append(token)
            else:
                _bad_tokens.append(token)
        fetched_providers_data[provider]['tokens'] = _res_tokens
        fetched_providers_data[provider]['bad_tokens'] = _bad_tokens
    return fetched_providers_data


def provider_data_merger(providers_tokens, out_dir="out"):
    """Sample Obj {"address": "0x006BeA43Baa3f7A6f765F14f10A1a1b08334EF45", "chainId": 1, "name": "Stox", "symbol": "STX", "decimals": 18, "logoURI": "https://tokens.1inch.io/0x006bea43baa3f7a6f765f14f10a1a1b08334ef45.png"}"""
    all_tokens = []
    chain_separated = {}
    chain_separated_and_merged_by_symbol = {}
    chain_separated_and_merged_by_name = {}

    for provider, items in providers_tokens.items():
        print(f"\nProvider: {provider}\n")
        for token in tqdm(items["tokens"]):

            if (chainId := token["chainId"]) not in chain_separated.keys():
                chain_separated[chainId] = {}
                chain_separated_and_merged_by_symbol[chainId] = {}
                chain_separated_and_merged_by_name[chainId] = {}

            if (
                token_symbol := token["symbol"]
            ) not in chain_separated_and_merged_by_symbol[chainId]:
                chain_separated_and_merged_by_symbol[chainId][token_symbol] = [
                ]

            if (token_name := token["name"]) not in chain_separated_and_merged_by_name[
                chainId
            ]:
                chain_separated_and_merged_by_name[chainId][token_name] = []

            if (token_address := token["address"]) not in chain_separated[chainId]:

                chain_separated[chainId][token_address] = {}
                chain_separated[chainId][token_address]["providers"] = []

            chain_separated[chainId][token_address].update(**token)

            chain_separated[chainId][token_address]["providers"].append(
                provider)
            chain_separated_and_merged_by_name[chainId][token_name].append(
                token)
            chain_separated_and_merged_by_symbol[chainId][token_symbol].append(
                token)
    for chain in chain_separated:
        for token in chain_separated[chain].values():
            all_tokens.append(token)

    with open(
        os.path.join(
            out_dir, "chain_separated_and_merged_by_symbol.json"), "w+"
    ) as f:
        json.dump(chain_separated_and_merged_by_symbol, f)

    with open(
        os.path.join(out_dir, "chain_separated_and_merged_by_name.json"), "w+"
    ) as f:
        json.dump(chain_separated_and_merged_by_name, f)

    with open(os.path.join(out_dir, "chain_separated.json"), "w+") as f:
        json.dump(chain_separated, f)

    return (
        chain_separated,
        chain_separated_and_merged_by_symbol,
        chain_separated_and_merged_by_name,
        all_tokens,
    )


def chainId_to_chain_name(chainId):
    chain = _CHAINS[int(chainId)]
    _ = str(chain.items()).lower()
    is_test_net = False
    for word in ["testnet", "test", "ropsten", "rinkby", "kovan", "test-net", "testy", "test net", "net-test"]:
        if word in _:
            is_test_net = True
            break
    return f"{'T' if  is_test_net else 'F'}:{chain['name']}-{chainId}"


def token_symbol_matcher(*args):
    token_symbols = dict()
    (
        chain_separated,
        chain_separated_and_merged_by_symbol,
        chain_separated_and_merged_by_name,
        all_tokens,
    ) = args
    for token in all_tokens:
        if (token_symbol := token["symbol"]) not in token_symbols:
            token_symbols[token_symbol] = []
        token_symbols[token_symbol].append(token)

    final_result = {}
    final_result_delete = {}
    print("\n----------------\nNow Input a Symbol to start searching!\n")
    while (user_input := input("[Symbol | 'q' ] >>> ")) != "q":
        user_selection = []
        user_selection_delete = []
        token_indices = sorted(
            [
                (i, symbol, fuzz.ratio(symbol, user_input), token, j)
                for i, (symbol, tokens) in enumerate(token_symbols.items())
                for j, token in enumerate(tokens)
            ],
            key=lambda x: float(x[2]),
            reverse=True,
        )
        print("Chose index of the symbol you think is correct:")
        i = 1
        print_detail = False
        while len(token_indices) > i * 8:
            sliced_res = token_indices[(8 * (i - 1)): 8 * i]
            print("\n".join(
                [
                    str(
                        {
                            "id": index, "t": _[1],
                            **(
                                _[3]
                                if print_detail
                                else
                                {"add": _[3]['address'], "chain":   chainId_to_chain_name(
                                    _[3]['chainId']), 'prov': _[3].get('providers')}
                            )
                        }
                    )
                    for index, _ in enumerate(sliced_res)]))
            answer = input(
                f"[{user_input}] [{len(user_selection)}] [id | (id,...) | 'a' / 'all' | 'det' | 'q' | 'c' | 'd' ] >>> ")
            match answer:
                case 'a' | 'all' | 'A':
                    user_selection.extend([(_[0], _[4]) for _ in sliced_res])
                    i += 1
                case 'q' | 'Q':
                    i += 1
                    break
                case 'det' | 'DET':
                    print_detail = True
                    continue
                case 'c' | 'C':
                    i += 1
                    continue
                case 'd' | 'D':
                    addr = input(
                        "Which ones you want to delete dear hossein ? : ")
                    try:
                        addr = eval(addr)
                        if isinstance(addr, int):
                            user_selection_delete.append(
                                (sliced_res[addr][0], sliced_res[addr][4]))
                        elif isinstance(addr, tuple | list | set):
                            user_selection_delete.extend(
                                [
                                    (sliced_res[_addr][0],
                                     sliced_res[_addr][4])
                                    for _addr in addr
                                ]
                            )
                    except:
                        print("Unkown Command !")

                case _:
                    if answer:
                        try:
                            answer = eval(answer)
                            if isinstance(answer, int):
                                user_selection.append(
                                    (sliced_res[answer][0], sliced_res[answer][4]))
                            elif isinstance(answer, tuple | list | set):
                                user_selection.extend(
                                    [
                                        (sliced_res[_answer][0],
                                         sliced_res[_answer][4])
                                        for _answer in answer
                                    ]
                                )
                        except:
                            print("Unkown Command !")
                    print_detail = False

        print("user_selection : ", user_selection)
        final_result[user_input] = []
        final_result_delete[user_input] = []

        for t_i in token_indices:
            for selection in user_selection:
                if selection[0] == t_i[0] and selection[1] == t_i[4]:
                    final_result[user_input].append(t_i[3])

        for t_i in token_indices:
            for selection in user_selection_delete:
                if selection[0] == t_i[0] and selection[1] == t_i[4]:
                    final_result_delete[user_input].append(t_i[3])

    with open(os.path.join("matched", f"match_res_{time.time()}.json"), "w+") as f:
        json.dump(final_result, f)

    with open(os.path.join("matched", f"delete_res_{time.time()}.json"), "w+") as f:
        json.dump(final_result_delete, f)


def take_a_dump(_: Any, reason=None):
    try:
        with open(f"{reason}pk.dump", "wb") as f:
            pickle.dump(_, f)

        with open(f"{reason}pk.dump", "rb") as f:
            _ = pickle.load(f)
    except Exception as e:
        print(" Failed at taking a dump")
    return _


if __name__ == "__main__":

    # print("\n####FETCHING TOKENS ....\n")

    # _vai_tokens()
    # fetch_tokens()

    print("\n####PROCESSING PROVIDER ....\n")

    _ = get_fetched_providers()  # type:ignore
    take_a_dump(_, "get_fetched_providers")

    print("\n####FIXING PROVIDER ....\n")
    _ = fix_fechted_providers(_)  # type:ignore
    take_a_dump(_, "fix_fechted_providers")

    print("\n####MERGING PROVIDER ....\n")
    _ = provider_data_merger(_)  # type:ignore
    take_a_dump(_, "provider_data_merger")

    print("\n####MATCHING TOKENS ....\n")
    token_symbol_matcher(*_)  # type:ignore
    take_a_dump(_, "token_symbol_matcher")
