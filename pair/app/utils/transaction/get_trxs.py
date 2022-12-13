from typing import List, Dict

from models import Chain, Trx
from utils.types import Address, ChainId


def get_user_all_token_trxs_len(address: Address) -> int:
    trx_len = 0
    for chain_id in Chain.supported_chains():
        chain_len = get_user_chain_token_trxs_len(chain_id, address)
        trx_len += chain_len
    return trx_len


def get_user_all_token_trxs(
    address: Address,
    skip: int,
    limit: int
) -> List[Trx]:
    trxs = []
    for chain_id in Chain.supported_chains():
        chain_trxs = get_user_chain_token_trxs(chain_id, address, skip, limit)
        if chain_trxs not in [None, []]:
            trxs.extend(chain_trxs)
    return trxs


def get_user_chain_token_trxs_len(
    chain_id: ChainId,
    address: Address,
) -> int:
    client = Trx.mongo_client(chain_id)
    query = {"userAddress": address}
    return len(list(client.find(query)))


def get_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address,
    skip: int,
    limit: int
) -> List[Trx]:
    client = Trx.mongo_client(chain_id)
    query = {"userAddress": address}

    if skip < 1:
        trxs = list(client.find(query).sort("timeStamp", -1).limit(limit))
    else:
        trxs = list(client.find(query).sort(
            "timeStamp", -1).skip(skip).limit(limit))

    return create_trx_objects(trxs)


def create_trx_objects(trxs: List[Dict]):
    trx_objs = []
    for trx in trxs:
        trx_objs.append(Trx(**trx))
    return trx_objs
