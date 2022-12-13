from typing import List, Dict
from pydantic import parse_obj_as

from models import Chain, Nft
from utils.types import Address, ChainId


def get_user_all_nfts_len(address: Address) -> int:
    nft_len = 0
    for chain_id in Chain.supported_chains():
        chain_len = get_user_chain_nfts_len(chain_id, address)
        nft_len += chain_len
    return nft_len


def get_user_all_nfts(
    address: Address,
    skip: int,
    limit: int
) -> List[Nft]:
    users_nfts = []
    for chain_id in Chain.supported_chains():
        chain_nfts = get_user_chain_nfts(chain_id, address, skip, limit)
        if chain_nfts not in [None, []]:
            users_nfts.extend(chain_nfts)

    return users_nfts


def get_user_chain_nfts_len(
    chain_id: ChainId,
    address: Address,
) -> int:
    client = Nft.mongo_client(chain_id)
    query = {"userAddress": address}
    return len(list(client.find(query)))


def get_user_chain_nfts(
    chain_id: ChainId,
    address: Address,
    skip: int,
    limit: int
) -> List[Nft]:
    client = Nft.mongo_client(chain_id)
    query = {"userAddress": address}

    if skip < 1:
        nfts = list(client.find(query).limit(limit))
    else:
        nfts = list(client.find(query).skip(skip).limit(limit))
    nfts = list(client.find(query)[skip:skip + limit])
    return create_nft_objects(nfts)


def create_nft_objects(nfts: List[Dict]):
    nft_objs = []
    for nft in nfts:
        nft_objs.append(parse_obj_as(Nft, nft))

    return nft_objs
