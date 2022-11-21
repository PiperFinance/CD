from typing import List

from models import Chain, Trx

def get_users_all_token_trxs(address: str) -> List[Trx]:
    trxs = []
    for chain_id in Chain.supported_chains():
        trxs.extend(get_users_chain_token_trxs(address, chain_id))
    return trxs


def get_users_chain_token_trxs(chain_id: int, address: str) -> List[Trx]:
    client = Trx.mongo_client(chain_id)
    query = {"userAddress":address}
    return client.find(query)