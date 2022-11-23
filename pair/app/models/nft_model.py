
from . import Chain
from configs.mongo_config import client

class Nft(Chain):
    userAddress: str
    address: str
    id: int
    name: str
    symbol: str
    decimal: int

    @classmethod
    def mongo_client(cls, chain_id: int):
        return client(cls.__class__.__name__, chain_id)



