import json
from typing import List, Dict, cast
from web3 import Web3
from pydantic import BaseModel

from configs.constant_config import constants
from utils.types import ChainId, Url, ApiKey, Web3, MongoClient, Name


class Chain(BaseModel):
    chainId: ChainId

    @staticmethod
    def supported_chains() -> List[ChainId]:
        return cast(List[ChainId], [250, 1, 3, 4, 5, 10, 42, 137, 42161, 42220, 80001])

    @property
    def dexs(self) -> List[Dict]:
        return constants.dexs[self.chainId]

    @property
    def tokens(self) -> List[Dict]:
        return constants.tokens[self.chainId]

    @property
    def chain_name(self) -> Name:
        return constants.chains[self.chainId]["name"]

    @property
    def url(self) -> Url:
        return constants.chains[self.chainId]["apiEndpoint"]

    @property
    def api_keys(self) -> List[ApiKey]:
        return constants.api_keys[self.chainId]

    @property
    def w3(self) -> Web3:
        rpc = constants.chains[self.chainId]["defaultRpcUrl"]
        return Web3(Web3.HTTPProvider(rpc))

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
