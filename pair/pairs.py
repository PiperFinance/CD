from web3 import Web3
import functools
import logging
from datetime import datetime
from typing import Optional, List, Set, Dict
from pydantic import BaseModel
import json
import requests
from schema.py import Pair, PairDetail, TokenDetail, Token

logger = logging.getLogger(__name__)


GECKO_TERMINAL = "https://app.geckoterminal.com/api/p1/pools"


def fetch_all_pairs() -> Dict[str, Pair]:
    readme_result = f"# PairParser @ {datetime.utcnow()=}"
    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BaseModel):
                return obj.dict()
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    dump = functools.partial(json.dump, cls=SetEncoder)

    def page_count():
        x = requests.get(GECKO_TERMINAL).json()
        return x['links']['last']['meta']['series'][-1]

    def page_result(page_number):
        return requests.get(
            GECKO_TERMINAL,
            {"include": "dex,dex.network,pool_metric,tokens",
             "page": page_number,
                # "include_network_metrics": True
             }
        ).json()

    r = []
    # NOTE - TO FETCH ALL TOKENS
    # for page_number in range(1, page_count()):
    #     try:
    #         r.append(page_result(page_number))
    #     except Exception as e:
    #         print(e)

    #  NOTE - already fetched once
    with open("pair/gecko_terminal_pools.json") as f:
        r = json.load(f)

    dexs = {}
    tokens = {}
    network = {}
    pool_metric = {}
    pools = {}
    dex_metrics = {}
    rel_types = ["dex", "token", "network", "pool_metric",  "pool"]

    results = {
        "pool": pools,
        "dex": dexs,
        "token": tokens,
        "network": network,
        "pool_metric": pool_metric,
        "dex_metric": dex_metrics,
    }
    count = 0
    _types = set()
    for result in r:
        for element in [*result['data'], *result['included']]:
            count += 1
            _types.add(element['type'])
            match element['type']:
                case "dex":
                    dexs[element['id']] = element
                case "dex_metric":
                    dex_metrics[element['id']] = element
                case "pool":
                    pools[element['id']] = element
                case "token":
                    tokens[element['id']] = element
                case "network":
                    network[element['id']] = element
                case "pool_metric":
                    pool_metric[element['id']] = element

    print(_types, count)
    readme_result += f"{_types=}\nall pool count:{count}\n"

    for _type in _types:
        type_result = results[_type]
        for type_id, type in type_result.items():
            if 'relationships' not in type:
                continue
            for rel_type, rel in type['relationships'].items():
                if rel_type in ['network_metric', 'dex_metric']:
                    continue
                rel_data = rel['data']
                if isinstance(rel_data, list):
                    for i, _elm in enumerate(rel_data):
                        _elem_id = _elm['id']
                        _elem_type = _elm['type']
                        if rel_type not in type_result[type_id] or isinstance(type_result[type_id].get(rel_type), list):
                            type_result[type_id][rel_type] = {}

                        type_result[type_id][rel_type][_elem_id] = results[_elem_type][_elem_id]
                else:
                    if rel_data['id'] not in results[rel_type]:
                        print(rel_data['id'], rel_type)
                    else:
                        type_result[type_id][rel_type] = results[rel_type][rel_data['id']]
            for rel_type in rel_types:
                if rel_type not in type_result[type_id]:
                    type_result[type_id][rel_type] = None
    _tmp = str({k: len(v) for k, v in results.items()})
    readme_result+=f"{_tmp}\n" 
    valid_tokens: Dict[str, Token] = {}

    for i, (token_id, token) in enumerate(tokens.items()):
        try:
            try:
                add = Web3.toChecksumAddress(token['attributes']['address'])
            except AttributeError:
                add = Web3.to_checksum_address(token['attributes']['address']) # type:ignore
                
            valid_tokens[token['id']] = Token(detail=TokenDetail(
                chainId=token['network']['attributes']['chain_id'],
                address=add,
                symbol=token['attributes']['symbol'],
                name=token['attributes']['name'],
                decimals=-1,
                logoURI=token['attributes']['image_url'],
                listedIn=None,
                lifiId=None,
                coingeckoId=None,
                tags=None,
                cmcId=None
            ))
        except ValueError as e:
            # print(token_id, token['network']['attributes']['chain_id'], e)
            pass
        except Exception as e:
            print(i)
            raise e

    readme_result += f"\n\n{len(valid_tokens)=}  errors {len(tokens)- len(valid_tokens)=}"

    valid_pools: Dict[str, Pair] = {}

    for i, (pool_id, pool) in enumerate(pools.items()):
        try:
            pool_tokens: Dict[str, Token] = {
                valid_tokens[_].detail.checksum: valid_tokens[_] for _ in pool['tokens']
            }
            
            try:
                add = Web3.toChecksumAddress(pool['attributes']['address'])
            except AttributeError:
                add = Web3.to_checksum_address(pool['attributes']['address']) # type:ignore

            valid_pools[pool['id']] = Pair(detail=PairDetail(
                chainId=pool['dex']['network']['attributes']['chain_id'],
                address=add,
                symbol=pool['dex']['attributes']['identifier'] +
                "LP (" + pool['attributes']['name'] + ")",
                name=pool['attributes']['name'],
                decimals=-1,
                dex=pool['dex']['attributes']['identifier'],
                tokens=pool_tokens,
                tokensOrder=list(pool_tokens.keys())
            ))
        except KeyError as e:
            # print(pool_id, pool['dex']['network']['attributes']['chain_id'], e)
            pass
        except ValueError as e:
            pass
        except Exception as e:
            # print(i)
            raise e

    chain_separated = {}
    count = 0

    for pair in valid_pools.values():
        # pair: Pair
        pair_det = pair.detail
        if pair_det.chainId not in chain_separated:
            chain_separated[pair_det.chainId] = []
        chain_separated[pair_det.chainId] = pair_det
        count += 1

    with open("pair/pairs_chain_separated.json", "w+") as f:
        dump(chain_separated, f)

    all_pairs = {_.detail.checksum: _ for _ in valid_pools.values()}
    with open("pair/all_pairs.json", "w+") as f:
        dump(all_pairs, f)

    readme_result += f"result {count=}"
    with open("pairs/README.md", "w+") as f:
        f.write(readme_result)
    return all_pairs
