import glob
from typing import Any, List, Dict, Set, Optional
import requests
import sys
import json
from datetime import datetime
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
from tokens import providers
from pydantic.json import pydantic_encoder
from schema import py as schema

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
OneMiB = 2**20
FILE_SIZE_SWEET_SPOT = {
    (0, 100): -10,
    (100, OneKiB): 10,
    (OneKiB, 100*OneKiB): 20,
    (100*OneKiB, OneMiB): 15,
    (OneMiB, 10*OneMiB): 7,
    (10*OneMiB, 100*OneMiB): -5
}


def logo_in_cache(token: schema.TokenDetail, out="./tmp"):
    for case, file_type in zip(
        [os.path.exists(f"{out}/{token.symbol}.svg"),
         os.path.exists(f"{out}/{token.symbol}.webp"),
         os.path.exists(f"{out}/{token.symbol}.png"),
         os.path.exists(f"{out}/{token.symbol}.jpg")],
            ['svg', 'webp', 'png', 'jpg']):
        if case:
            return f"{token.symbol}.{file_type}"


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


res_req: dict = {}
res_type: dict = {}


def chose(options, symbol=None, try_request=False, base_url=None, out="./tmp"):
    options_weight: dict = {}
    for option in options:

        if option not in options_weight:
            options_weight[option] = 0

        if try_request:
            try:
                if option in res_req:
                    r = res_req[option]
                else:
                    file_name, file_type = check_file(option)
                    file_dir = os.path.join(
                        out, "tmp", "~".join([symbol or "", file_name]))
                    # CHECK FILE
                    print(file_dir)
                    if os.path.exists(file_dir):
                        print(file_dir)
                        with open(file_dir, "rb") as f:
                            r = f.read()
                    else:
                        r = requests.get(option)
                        if r.status_code == 200:
                            res_req[option] = r.content
                            with open(file_dir, "wb+") as f:
                                f.write(r.content)
                        else:
                            res_req[option] = None

                if res_req.get(option):
                    img_content = res_req[option]
                    file_name, file_type = check_file(option)
                    options_weight[option] += check_file_size(img_content)
                    options_weight[option] += check_file_type(option)
                    res_type[option] = file_type

            except Exception as e:
                continue

        options_weight[option] += 1
    if options_weight:
        _chosen_option, _chosen_score = sorted(options_weight.items(),
                                               key=lambda x: x[1], reverse=True)[0]

        if not try_request:
            return _chosen_option
        elif _chosen_score > 0 and symbol and _chosen_option in res_req and _chosen_option in res_type:

            print(f"Chosen {_chosen_option} with score of {_chosen_score}")
            _file_name = f"{symbol}.{res_type[_chosen_option]}"
            with open(os.path.join(out, _file_name), "wb+") as f:
                f.write(res_req[_chosen_option])
            return f"{base_url}/{_file_name}"
        else:
            return _chosen_option


def provider_data_merger(
        providers_tokens: Dict[str, providers.Provider],
        out_dir="out",
        verify=None,
        include_testnet=False,
        find_logo_in_cache=True,
        try_request_token_logo=False,
        token_logoURI_BaseURL=None,
        result_readme_file=sys.stdout,
        avoid_addresses: Optional[Set[str]] = None
):
    """
    Merges given providers
    Tokens follow schema.TokenDetail
    Exceptions:
    - Natives
    - StableCoins
        - CMC-SC

    # Token Logo is fetched and saved into a directory
    - token_logoURI_BaseURL : For logo base url (e.g. https://raw.githubusercontent.com/PiperFinance/LO/main/logo)
    - try_request_token_logo: For request token logo from those chains
    """
    if avoid_addresses is None:
        avoid_addresses = set()
    # For Having everything all at once
    all_tokens_providers: Dict[schema.TokenDetail, List[str]] = {}
    all_tokens_logo: Dict[schema.TokenDetail, List[str]] = {}
    all_tokens_tags: Dict[schema.TokenDetail, List[str]] = {}
    all_tokens_lifiId: Dict[schema.TokenDetail, List[str]] = {}
    all_tokens_coingeckoId: Dict[schema.TokenDetail, List[str]] = {}

    all_tokens: Dict[str, schema.Token] = {}
    # For Go portfolio scanner ...
    chain_separated_v2: List[schema.ChainToken] = list()

    chain_separated: Dict[int, set[schema.Token]] = {}
    chain_separated_and_merged_by_tokenId: Dict[int,
                                                Dict[str, List[schema.Token]]] = {}
    # For Human readable style of merging tokens ...
    chain_separated_and_merged_by_symbol: Dict[int,
                                               Dict[str, List[schema.TokenDetail]]] = {}
    chain_separated_and_merged_by_name: Dict[int,
                                             Dict[str, List[schema.TokenDetail]]] = {}

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
    for token, token_providers in tqdm(all_tokens_providers.items()):
        if token.address in avoid_addresses:
            continue
        token: schema.TokenDetail
        token.listedIn = token_providers
        if len(token.listedIn) > MIN_LISTED_COUNT:
            token.verify = True
            verified_count += 1
        token.coingeckoId = chose(all_tokens_coingeckoId[token])
        token.lifiId = chose(all_tokens_lifiId[token])
        token.tags = list(set(all_tokens_tags[token]))
        if find_logo_in_cache:
            token.logoURI = logo_in_cache(token, "./logo")
            if token.logoURI is not None:
                token.logoURI = f"{token_logoURI_BaseURL}/{token.logoURI}"

        elif try_request_token_logo:
            token.logoURI = chose(
                all_tokens_logo[token],
                symbol=token.symbol,
                try_request=try_request_token_logo,
                base_url=token_logoURI_BaseURL,
                out="./logo")

        if (  # Following Providers are exceptions
            "Natives" not in token.listedIn
            and "CMC-SC" not in token.listedIn
        ) and verify is not None:
            if verify == token.verify:
                all_tokens[token.checksum] = schema.Token(detail=token)
        else:
            all_tokens[token.checksum] = schema.Token(detail=token)

    for _token in tqdm(all_tokens.values()):
        token = _token.detail
        if (chainId := token.chainId) not in chain_separated_and_merged_by_tokenId:
            chain_separated[chainId] = set()
            chain_separated_and_merged_by_symbol[chainId] = {}
            chain_separated_and_merged_by_name[chainId] = {}
            chain_separated_and_merged_by_tokenId[chainId] = {}

        if (token_symbol := token.symbol) not in chain_separated_and_merged_by_symbol[chainId]:
            chain_separated_and_merged_by_symbol[chainId][token_symbol] = []
        if (token_name := token.name) not in chain_separated_and_merged_by_name[chainId]:
            chain_separated_and_merged_by_name[chainId][token_name] = []
        if (token_address := token.checksum) not in chain_separated_and_merged_by_tokenId[chainId]:
            chain_separated_and_merged_by_tokenId[chainId][token.checksum] = []
        chain_separated_and_merged_by_tokenId[chainId][token.checksum].append(
            schema.Token(detail=token))
        chain_separated_and_merged_by_name[chainId][token_name].append(token)
        chain_separated_and_merged_by_symbol[chainId][token_symbol].append(
            token)
        # if (get_from_list(chain_separated[chainId], token))
        chain_separated[chainId].add(schema.Token(detail=token))

    result_readme = ""
    result_readme += (f"# TokenResult Parsed @ {datetime.now()} \n\n## Result \n ::: {len(chain_separated)} chains  ::: {verified_count} verified ::: {len(all_tokens)} total_saved ::: {literally_all_tokens_count - len(all_tokens)} duplicates ::: \n")
    for chain, tokens in chain_separated.items():
        result_readme += (
            f"- {chain}  :::  {_CHAINS[chain]['name']}  :::  {len(tokens)} :::  { {provider for token in tokens for provider in (token.detail.listedIn or [])  } } \n")
    print(result_readme, file=result_readme_file, flush=True)
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
        dump(chain_separated_and_merged_by_tokenId, f)

    with open(os.path.join(out_dir, "all_tokens.json"), "w+") as f:
        dump(all_tokens, f)

    return (
        chain_separated_and_merged_by_tokenId,
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
