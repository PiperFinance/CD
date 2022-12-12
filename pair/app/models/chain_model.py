import json
from typing import List, cast
from web3 import Web3
from pydantic import BaseModel

from utils.types import ChainId, Url, ApiKey, Web3, MongoClient, Name


class Chain(BaseModel):
    chainId: ChainId

    @staticmethod
    def supported_chains() -> List[ChainId]:
        return cast(List[ChainId], [250, 1, 3, 4, 5, 10, 42, 137, 42161, 42220, 80001])

    @property
    def chain_name(self) -> Name:
        with open("utils/chains.json") as f:
            chains = json.load(f)
            return chains[str(self.chainId)]["name"]

    @property
    def url(self) -> Url:
        with open("utils/chains.json") as f:
            chains = json.load(f)
            return chains[str(self.chainId)]["apiEndpoint"]

    @property
    def api_keys(self) -> List[ApiKey]:
        with open("utils/chains.json") as f:
            chains = json.load(f)
            return chains[str(self.chainId)]["apiKeys"]

    @property
    def w3(self) -> Web3:
        with open("utils/chains.json") as f:
            chains = json.load(f)
            rpc = chains[str(self.chainId)]["defaultRpcUrl"]
        return Web3(Web3.HTTPProvider(rpc))

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
