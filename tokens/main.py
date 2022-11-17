import os
import json
import glob
import time
import logging
import requests
import difflib
from pathlib import Path
from web3 import Web3 #type:ignore
from thefuzz import fuzz #type:ignore
from tqdm import tqdm

logger = logging.getLogger(__name__)


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
            r[file.replace(".json", "").split("/")[-1]] = json.load(f)
    return r


def check_token_data(token):
    _add = token['address'] 
    match _add:
        case "0xaa44051bdd76e251aab66dbbe82a97343b4d7da3#code":
            _add = '0xaa44051bdd76e251aab66dbbe82a97343b4d7da3'
        case "0x77F86D401e067365dD911271530B0c90DeC3e0f7/":
            _add = "0x77F86D401e067365dD911271530B0c90DeC3e0f7"
        case "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2#balances":
            _add = "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2"
        
    token['address'] = Web3.toChecksumAddress(_add)
    return token

def provider_parser(providers_tokens, out_dir="out"):
    """Sample Obj {"address": "0x006BeA43Baa3f7A6f765F14f10A1a1b08334EF45", "chainId": 1, "name": "Stox", "symbol": "STX", "decimals": 18, "logoURI": "https://tokens.1inch.io/0x006bea43baa3f7a6f765f14f10a1a1b08334ef45.png"}"""
    all_tokens = []
    chain_separated = {}
    chain_separated_and_merged_by_symbol = {}
    chain_separated_and_merged_by_name = {}

    for provider, items in tqdm(providers_tokens.items()):
        for _token in tqdm(items["tokens"]):
            token = check_token_data(_token)
            if (chainId := token["chainId"]) not in chain_separated.keys():
                chain_separated[chainId] = {}
                chain_separated_and_merged_by_symbol[chainId] = {}
                chain_separated_and_merged_by_name[chainId] = {}

            if (
                token_symbol := token["symbol"]
            ) not in chain_separated_and_merged_by_symbol[chainId]:
                chain_separated_and_merged_by_symbol[chainId][token_symbol] = []

            if (token_name := token["name"]) not in chain_separated_and_merged_by_name[
                chainId
            ]:
                chain_separated_and_merged_by_name[chainId][token_name] = []

            if (token_address := token["address"]) not in chain_separated[chainId]:
                
                chain_separated[chainId][token_address] = {}
                chain_separated[chainId][token_address]["providers"] = []
            
            
            chain_separated[chainId][token_address].update(**token)
            
            chain_separated[chainId][token_address]["providers"].append(provider)
            chain_separated_and_merged_by_name[chainId][token_name].append(token)
            chain_separated_and_merged_by_symbol[chainId][token_symbol].append(token)
    for chain in chain_separated:
        for token in  chain_separated[chain].values():
            all_tokens.append(token)
        

    with open(
        os.path.join(out_dir, "chain_separated_and_merged_by_symbol.json"), "w+"
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
with open( os.path.join(Path(os.getcwd()).parent.absolute(), "chains" , "chains.json")) as f:
    _CHAINS = { int(c['chainId']) : c for c in json.load(f)}
     
def chainId_to_chain_name(chainId):
    return _CHAINS[int(chainId)]['name'] 


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
    print("\n----------------\nNow Input a Symbol to start searching!\n")
    while (user_input := input("[Symbol | 'q' ] >>> ")) != "q":
        user_selection = []
        token_indices = sorted(
            [
                (i, symbol, fuzz.ratio(symbol, user_input), token, j)
                for i, (symbol , tokens) in enumerate(token_symbols.items())
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
                            "id":index, "t":_[1], 
                        **(
                            _[3]
                            if print_detail
                            else
                            {"add" : _[3]['address'], "chain":   chainId_to_chain_name(_[3]['chainId']) , 'prov' : _[3].get('providers') }
                        )
                        }
                        ) 
                                 for index , _ in  enumerate(sliced_res)]))
            answer = input(f"[{user_input}] [{len(user_selection)}] [id | (id,...) | 'a' / 'all' | 'det' | 'q' ] >>> ")
            i += 1
            match answer:
                case 'a' | 'all':
                    user_selection.extend([(_[0], _[4]) for _ in sliced_res])
                case 'q':
                    break                    
                case 'det':
                    print_detail = True
                    i -= 1
                    continue

                case _ :
                    if answer:
                        answer = eval(answer)
                        if isinstance(answer, int): 
                            user_selection.append((sliced_res[answer][0] , sliced_res[answer][4]))
                        elif isinstance(answer, tuple | list | set ):
                            user_selection.extend(
                                [
                                    (sliced_res[_answer][0] , sliced_res[_answer][4])
                                    for _answer in answer
                                    ]
                                )
                    print_detail = False
                    
        print("user_selection : ", user_selection)
        final_result[user_input] = []
        for t_i in token_indices:
            for selection in user_selection:
                if selection[0] == t_i[0] and  selection[1] == t_i[4]:
                    final_result[user_input].append(t_i[3])

    with open(f"match_res_{time.time()}.json","w") as f:
        json.dump(final_result,f)
                    
                    
                        
                


if __name__ == "__main__":

    # print("\n####FETCHING TOKENS ....\n")
    
    # fetch_tokens()
    
    print("\n####PROCESSING TOKENS ....\n")

    _ = get_fetched_providers()

    print("\n####PROCESSING TOKENS ....\n")

    _ = provider_parser(_)

    print("\n####MATCHING TOKENS ....\n")
    token_symbol_matcher(*_)
