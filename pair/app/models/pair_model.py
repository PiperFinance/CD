from typing import List, Optional

from . import Chain
from configs.mongo_config import client
from utils.types import Address, BigInt, Price, ChainId, Name, Decimal, MongoClient


class Pair(Chain):
    address: Address
    name: Name
    dex: Name
    decimals: List[Decimal]
    reserves: List[BigInt]
    totalSupply: BigInt
    price: Optional[Price]

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        return client(cls.__class__.__name__, chain_id)
