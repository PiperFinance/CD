from typing import List, Dict
from models import Chain, Pair

from utils.types import ChainId


def get_all_pairs_len():
    pair_len = 0
    for chain_id in Chain.supported_chains():
        pair_len += get_chain_pairs_len(chain_id)
    return pair_len


def get_all_pairs(
    skip: int,
    limit: int
):
    pairs = []
    for chain_id in Chain.supported_chains():
        chain_pairs = get_chain_pairs(chain_id, skip, limit)
        if chain_pairs not in [None, []]:
            pairs.extend()

    return pairs


def get_chain_pairs_len(chain_id: ChainId) -> int:
    client = Pair.mongo_client(chain_id)
    return len(list(client.find()))


def get_chain_pairs(
    chain_id: int,
    skip: int,
    limit: int
):
    client = Pair.mongo_client(chain_id)
    if skip < 1:
        pairs = list(client.find().limit(limit))
    else:
        pairs = list(client.find().skip(skip).limit(limit))
    return create_pair_objects(pairs)


def create_pair_objects(pairs: List[Dict]):
    pair_objs = []
    for pair in pairs:
        pair_objs.append(Pair(**pair))
    return pair_objs
