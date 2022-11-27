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

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        return client(cls.__class__.__name__, chain_id)
