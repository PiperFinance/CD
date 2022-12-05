from typing import Optional
from enum import Enum

from . import Chain
from configs.mongo_config import client
from utils.types import (
    Address,
    ChainId,
    Id,
    Symbol,
    Name,
    Decimal,
    Price,
    MongoClient
)


class NftType(Enum):
    ERC721 = 721
    ERC1155 = 1155


class Nft(Chain):
    userAddress: Address
    address: Address
    id: Id
    name: Optional[Name]
    symbol: Optional[Symbol]
    decimal: Decimal
    price: Optional[Price]
    uri: Optional[str]
    verified: bool = False
    type: Optional[int]

    @staticmethod
    def mongo_client(chain_id: ChainId) -> MongoClient:
        return client("NFT", chain_id)
