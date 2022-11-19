from . import Chain
from configs.mongo_config import client

class Trx(Chain):
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

    @property
    def description(self):
        x = self.__class__.__name__
        return client(self.__class__.__name__, self.chainId)



