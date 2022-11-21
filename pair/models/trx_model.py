from typing import List, Optional

from . import Chain
from configs.mongo_config import client

class Trx(Chain):
    userAddress: str
    labels: Optional[List[str]]
    blockNumber: str
    timeStamp: str
    hash: str
    nonce: str
    blockHash: str
    fromAddress: str
    contractAddress: str
    to: str
    value: str
    tokenName: str
    tokenSymbol: str
    tokenDecimal: str
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    input: str
    confirmations: str

    @classmethod
    def mongo_client(cls, chain_id: int):
        return client(cls.__class__.__name__, chain_id)



