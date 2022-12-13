from pydantic import BaseModel
from typing import Union, Optional, List
from schema.py.others import *
from schema.py.Chain import Chain


class Label(BaseModel):
    title: str
    value: Union[str, int]


class Trx(Chain):
    userAddress: Address
    labels: Optional[List[Label]]
    blockNumber: StringBlockNumber
    timeStamp: int
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
