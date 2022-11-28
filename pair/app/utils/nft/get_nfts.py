from typing import List, Dict

from models import Chain, Nft
from utils.types import Address, ChainId


def get_users_all_nfts(address: Address) -> List[Nft]:
    users_nfts = []
    for chain_id in Chain.supported_chains():
        users_nfts.extend(get_users_chain_nfts(address, chain_id))

    return users_nfts


def get_users_chain_nfts(chain_id: ChainId, address: Address) -> List[Nft]:
    client = Nft.mongo_client(chain_id)
    query = {"userAddress": address}
    nfts = list(client.find(query))
    return create_nft_objects(nfts)


def create_nft_objects(nfts: List[Dict]):
    nft_objs = []
    for nft in nfts:
        nft_objs.append(Nft(**nft))

    return nft_objs
