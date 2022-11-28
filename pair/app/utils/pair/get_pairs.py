from typing import List, Dict
from models import Chain, Pair


def get_all_pairs():
    pairs = []
    for chain_id in Chain.supported_chains():
        pairs.extend(get_chain_pairs(chain_id))


def get_chain_pairs(chain_id: int):
    client = Pair.mongo_client(chain_id)
    pairs = list(client.find())
    return create_pair_objects(pairs)


def create_pair_objects(pairs: List[Dict]):
    pair_objs = []
    for pair in pairs:
        pair_objs.append(Pair(**pair))
    return pair_objs
