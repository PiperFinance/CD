from typing import List

from models import Chain, Nft


def get_users_all_nfts(address: str) -> List[Nft]:
    users_nfts = []
    for chain_id in Chain.supported_chains():
        users_nfts.extend(get_users_chain_nfts(address, chain_id))

    return users_nfts


def get_users_chain_nfts(chain_id: int, address: str) -> List[Nft]:
    client = Nft.mongo_client(chain_id)
    query = {"userAddress": address}
    return client.find(query)
