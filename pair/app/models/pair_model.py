from typing import List, Optional

from . import Chain
from configs.mongo_config import client



class Pair(Chain):
    address: str
    name: str
    dex: str
    decimals: List[int]
    reserves: List[str]
    totalSupply: str
    price: Optional[str]

    @classmethod
    def mongo_client(cls, chain_id: int):
        return client(cls.__class__.__name__, chain_id)
