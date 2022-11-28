from . import Chain
from configs.mongo_config import client
from utils.types import Address, ChainId, Id, Symbol, Name, Decimal, MongoClient

class Nft(Chain):
    userAddress: Address
    address: Address
    id: Id
    name: Name
    symbol: Symbol
    decimal: Decimal

    @staticmethod
    def mongo_client(chain_id: ChainId) -> MongoClient:
        return client("NFT", chain_id)
