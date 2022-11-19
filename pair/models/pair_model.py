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

    @property
    def mongo_client(self):
        return client(self.__class__.__name__, self.chainId)
