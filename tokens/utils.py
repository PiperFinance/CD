from typing import Any, List, Dict, Set
import requests
import json
import functools
import logging
from pydantic import BaseModel
import os
import pickle
import time
from pathlib import Path
from thefuzz import fuzz
from tqdm import tqdm
from web3 import Web3
from tokens import schema
from tokens import providers
from pydantic.json import pydantic_encoder

logger = logging.getLogger(__name__)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.dict()
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


dump = functools.partial(json.dump, cls=SetEncoder)


# Token ABI
with open("abi/token.abi") as f:
    TOKEN_ABI = json.load(f)


# Create Token contract objects  and w3 connections ...
# use _W3s for w3 : map [chainId : int , w3]
# use _CONTRACTS for w3 : map [chainId : int , contract obj]
with open(os.path.join(Path(os.getcwd()), "chains", "mainnet.json")) as f:
    mainnet_chains = json.load(f)
    _CHAINS = {int(c['id']): c for c in mainnet_chains}
    _MAINNET_CHAINS_ID = {int(c['id']) for c in mainnet_chains}

    _CONTRACTS = {}
    for chain in mainnet_chains:
        rpc = chain.get('rpcUrls')['default']
        if "${INFURA_API_KEY}" in rpc:
            rpc = rpc.replace("${INFURA_API_KEY}",
                              "31d72a42f19f4a39a6d831f8b331f875")
        w3 = Web3(Web3.HTTPProvider(rpc))

        def _(_address, _w3=w3):
            return _w3.eth.contract(_address, abi=TOKEN_ABI)  # type: ignore
        _CONTRACTS[int(chain['id'])] = _


def get_from_list(items: list, item, default=None):
    for _item in items:
        if hash(_item) == hash(item):
            return _item
    else:
        return default


MIN_LISTED_COUNT = 2
global verified_count, literally_all_tokens_count
verified_count = 0
literally_all_tokens_count = 0


SUPPORTED_IMG_FILE_FORMAT = {
    "svg": 15,
    "webp": 15,
    "png": 10,
    "jpg": 5,
}
# NOTE - file size category in bytes
OneKiB = 2**10
OneMiB = 2**10
FILE_SIZE_SWEET_SPOT = {
    (0, 100): 1,
    (100, OneKiB): 10,
    (OneKiB, 100*OneKiB): 20,
    (100*OneKiB, OneMiB): 15,
    (OneMiB, 10*OneMiB): 7,
    (10*OneMiB, 100*OneMiB): -5
}


def check_file(option: str):

    for file_type in SUPPORTED_IMG_FILE_FORMAT:
        if file_type in option:
            token_url_name = option.split("/")[-1]
            index = token_url_name.index(file_type)
            return token_url_name[:(index + len(file_type))], file_type
    return option.split("/")[-1], ""


def check_file_type(option):
    for file_type, score in SUPPORTED_IMG_FILE_FORMAT.items():
        if file_type in option:
            return score
    return -10


def check_file_size(img_content):
    img_size = len(img_content)
    for (min_size, max_size), score in FILE_SIZE_SWEET_SPOT.items():
        if img_size > min_size and img_size <= max_size:
            return score
    return -10


def chose(options, symbol=None, try_request=False, out="./tmp"):
    options_weight: dict = {}
    res_file: dict = {}
    res_type: dict = {}
    for option in options:

        if option not in options_weight:
            options_weight[option] = 0

        if try_request:

            try:
                r = requests.get(option)
                if r.status_code < 300:
                    img_content = r.content
                    file_name, file_type = check_file(option)
                    file_dir = os.path.join(
                        out, "tmp", "~".join([symbol or "", file_name]))
                    options_weight[option] += check_file_size(img_content)
                    options_weight[option] += check_file_type(option)
                    with open(file_dir, "wb+") as f:
                        f.write(img_content)
                        res_file[option] = img_content
                    res_type[option] = file_type
                else:
                    continue
            except Exception as e:
                print(e)
                continue
        options_weight[option] += 1
    if options_weight:
        _chosen_option, _chosen_score = sorted(options_weight.items(),
                                               key=lambda x: x[1], reverse=True)[0]
        print(f"Chosen {_chosen_option} with score of {_chosen_score}")

        if try_request and symbol:

            with open(os.path.join(out, f"{symbol}.{res_type[_chosen_option]}"), "wb+") as f:
                f.write(res_file[_chosen_option])
        return _chosen_option
    del res_file
    del res_type


def provider_data_merger(
        providers_tokens: Dict[str, providers.Provider], out_dir="out", verify=None, include_testnet=False):
    """
    Merges given providers
    Tokens follow schema.Token     
    Exceptions:
    - Natives
    - StableCoins 
        - CMC-SC
    """
    # For Having everything all at once
    all_tokens_providers: Dict[schema.Token, List[str]] = {}
    all_tokens_logo: Dict[schema.Token, List[str]] = {}
    all_tokens_tags: Dict[schema.Token, List[str]] = {}
    all_tokens_lifiId: Dict[schema.Token, List[str]] = {}
    all_tokens_coingeckoId: Dict[schema.Token, List[str]] = {}

    all_tokens: List[schema.Token] = []
    # For Go portfolio scanner ...
    chain_separated_v2: List[schema.ChainToken] = list()

    chain_separated: Dict[int, set[schema.Token]] = {}
    chain_separated_and_merged_by_address: Dict[int,
                                                Dict[str, List[schema.Token]]] = {}
    # For Human readable style of merging tokens ...
    chain_separated_and_merged_by_symbol: Dict[int,
                                               Dict[str, List[schema.Token]]] = {}
    chain_separated_and_merged_by_name: Dict[int,
                                             Dict[str, List[schema.Token]]] = {}

    global verified_count, literally_all_tokens_count

    # Get All tokens in a list from all providers ...
    # Also
    # - checks for testnet tokens is asked in kwargs
    # - checks Optional fields like
    #  - Logo
    #  - tags
    #  - lifiId
    #  - Coingecko
    for provider, items in providers_tokens.items():
        print(f"\nProvider: {provider}\n")
        literally_all_tokens_count += len(items.tokens)
        for token in tqdm(items.tokens):
            if (not include_testnet) and token.chainId not in _MAINNET_CHAINS_ID:
                continue
            if token not in all_tokens_providers:
                all_tokens_logo[token] = []
                all_tokens_tags[token] = []
                all_tokens_lifiId[token] = []
                all_tokens_providers[token] = []
                all_tokens_coingeckoId[token] = []
            all_tokens_providers[token].append(provider)
            # NOTE - Later check if following optional fields match ...
            if token.tags:
                all_tokens_tags[token].extend(token.tags)
            if token.logoURI:
                all_tokens_logo[token].append(token.logoURI)
            if token.lifiId:
                all_tokens_lifiId[token].append(token.lifiId)
            if token.coingeckoId:
                all_tokens_coingeckoId[token].append(token.coingeckoId)

    # Remove Unverified tokens from list and
    for token, token_providers in all_tokens_providers.items():
        token: schema.Token
        token.listedIn = token_providers
        if len(token.listedIn) > MIN_LISTED_COUNT:
            token.verify = True
            verified_count += 1
        token.logoURI = chose(
            all_tokens_logo[token], symbol=token.symbol, try_request=True, out="./logo")
        token.coingeckoId = chose(all_tokens_logo[token])
        token.lifiId = chose(all_tokens_logo[token])
        token.tags = chose(all_tokens_logo[token])
        if (  # Following Providers are exceptions
            "Natives" not in token.listedIn
            and "CMC-SC" not in token.listedIn
        ) and verify is not None:
            if verify == token.verify:
                all_tokens.append(token)
        else:
            all_tokens.append(token)

    for token in tqdm(all_tokens):
        if (chainId := token.chainId) not in chain_separated_and_merged_by_address:
            chain_separated[chainId] = set()
            chain_separated_and_merged_by_symbol[chainId] = {}
            chain_separated_and_merged_by_name[chainId] = {}
            chain_separated_and_merged_by_address[chainId] = {}

        if (token_symbol := token.symbol) not in chain_separated_and_merged_by_symbol[chainId]:
            chain_separated_and_merged_by_symbol[chainId][token_symbol] = []
        if (token_name := token.name) not in chain_separated_and_merged_by_name[chainId]:
            chain_separated_and_merged_by_name[chainId][token_name] = []
        if (token_address := token.address) not in chain_separated_and_merged_by_address[chainId]:
            chain_separated_and_merged_by_address[chainId][token_address] = []
        chain_separated_and_merged_by_address[chainId][token_address].append(
            token)
        chain_separated_and_merged_by_name[chainId][token_name].append(token)
        chain_separated_and_merged_by_symbol[chainId][token_symbol].append(
            token)
        # if (get_from_list(chain_separated[chainId], token))
        chain_separated[chainId].add(token)

    print(f"\n\n --- Result ::: {len(chain_separated)} chains  ::: {verified_count} verified ::: {len(all_tokens)} total_saved ::: {literally_all_tokens_count - len(all_tokens)} duplicates ::: Chains :\n")
    for chain, tokens in chain_separated.items():
        print(
            f" \t --- {chain}  :::  {_CHAINS[chain]['name']}  :::  {len(tokens)} :::  { {provider for token in tokens for provider in (token.listedIn or [])  } }")
    for chain, tokens in chain_separated.items():
        # for token in chain_separated[chain].values():
        #     chain_tokens.append(token)

        chain_separated_v2.append(schema.ChainToken(**{
            "chainId": chain,
            "tokens": list(tokens)
        }))

    with open(
        os.path.join(
            out_dir, "chain_separated_v2.json"), "w+"
    ) as f:
        dump(chain_separated_v2, f)

    with open(
        os.path.join(
            out_dir, "chain_separated_and_merged_by_symbol.json"), "w+"
    ) as f:
        dump(chain_separated_and_merged_by_symbol, f)

    with open(
        os.path.join(out_dir, "chain_separated_and_merged_by_name.json"), "w+"
    ) as f:
        dump(chain_separated_and_merged_by_name, f)

    with open(os.path.join(out_dir, "chain_separated.json"), "w+") as f:
        dump(chain_separated_and_merged_by_address, f)

    with open(os.path.join(out_dir, "all_tokens.json"), "w+") as f:
        dump(all_tokens, f)

    return (
        chain_separated_and_merged_by_address,
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
        if (token_symbol := token.symbol) not in token_symbols:
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
        if _ is not None:
            with open(f"{reason}pk.dump", "wb") as f:
                pickle.dump(_, f)

        with open(f"{reason}pk.dump", "rb") as f:
            _ = pickle.load(f)
    except Exception as e:
        print(" Failed at taking a dump")
    return _


COIN_GECKO_LIST_MAX_AGE = 3600


if __name__ == "__main__":

    # print("\n####FETCHING TOKENS ....\n")

    # _vai_tokens()
    # fetch_tokens()

    # print("\n####PROCESSING PROVIDER ....\n")

    # _ = get_fetched_providers()  # type:ignore
    # take_a_dump(_, "get_fetched_providers")

    # print("\n####FIXING PROVIDER ....\n")
    # _ = fix_fechted_providers(_)  # type:ignore
    # take_a_dump(_, "fix_fechted_providers")

    # print("\n####MERGING PROVIDER ....\n")
    # _ = provider_data_merger(_)  # type:ignore
    # take_a_dump(_, "provider_data_merger")

    # print("\n####MATCHING TOKENS ....\n")
    # token_symbol_matcher(*_)  # type:ignore
    # take_a_dump(_, "token_symbol_matcher")

    # _ = take_a_dump(None, "token_symbol_matcher")
    # (
    #     chain_separated,
    #     chain_separated_and_merged_by_symbol,
    #     chain_separated_and_merged_by_name,
    #     all_tokens
    # ) = _
    # with open("_tokens.json", "w") as f:
    #     json.dump(
    #         list(chain_separated[1].values()),
    #         f
    #     )

    ...
