from pydantic import BaseModel
from typing import List, Optional, Union

from . import Chain
from configs.mongo_config import client
from utils.types import Address, StringBlockNumber, StringTimestamp, Symbol, Name, Decimal, MongoClient


class Label(BaseModel):
    title: str
    value: Union[str, int]


class Trx(Chain):
    userAddress: Address
    labels: Optional[List[Label]]
    blockNumber: StringBlockNumber
    timeStamp: StringTimestamp
    hash: str
    nonce: str
    blockHash: str
    fromAddress: Address
    contractAddress: Address
    to: Address
    value: str
    tokenName: Name
    tokenSymbol: Symbol
    tokenDecimal: Decimal
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    input: str
    confirmations: str

    @classmethod
    def mongo_client(cls, chain_id: int) -> MongoClient:
        return client(cls.__class__.__name__, chain_id)
