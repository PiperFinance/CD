from typing import Optional
from enum import Enum

from . import Chain
from configs.mongo_config import client
from utils.types import (
    Address,
    ChainId,
    Symbol,
    Name,
    Price,
    MongoClient
)


class NftType(Enum):
    ERC721 = 721
    ERC1155 = 1155


class Nft(Chain):
    userAddress: Address
    address: Address
    id: str
    name: Optional[Name]
    symbol: Optional[Symbol]
    description: Optional[str]
    price: Optional[Price]
    uri: Optional[str]
    verified: bool = False
    type: Optional[int]
    idAddress: str
    balance: int
    totalSupply: int

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        c = client(cls.__name__, chain_id)
        c.create_index(
            "idAddress",
            unique=True
        )
        return c
