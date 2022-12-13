from typing import List, Optional, Tuple

from . import Chain
from configs.mongo_config import client
from utils.types import Address, BigInt, ChainId, Name, Decimal, MongoClient


class Pair(Chain):
    address: Address
    name: Name
    dex: Name
    chainId: ChainId
    tokens: Tuple[Address, Address]
    decimals: List[Decimal]
    reserves: List[BigInt]
    totalSupply: BigInt
    price: Optional[BigInt]

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        c = client(cls.__name__, chain_id)
        c.create_index(
            "address",
            unique=True
        )
        return c
