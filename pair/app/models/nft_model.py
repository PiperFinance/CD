from typing import Optional

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


class Nft(Chain):
    userAddress: Address
    address: Address
    id: Id
    name: Name
    symbol: Symbol
    decimal: Decimal
    price: Optional[Price]
    uri: Optional[str]
    verified: bool = False

    @staticmethod
    def mongo_client(chain_id: ChainId) -> MongoClient:
        return client("NFT", chain_id)
