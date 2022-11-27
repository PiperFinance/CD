from typing import List

from models import Chain, Trx
from utils.types import Address, ChainId


def get_users_all_token_trxs(address: Address) -> List[Trx]:
    trxs = []
    for chain_id in Chain.supported_chains():
        trxs.extend(get_users_chain_token_trxs(address, chain_id))
    return trxs


def get_users_chain_token_trxs(chain_id: ChainId, address: Address) -> List[Trx]:
    client = Trx.mongo_client(chain_id)
    query = {"userAddress":address}
    return client.find(query)