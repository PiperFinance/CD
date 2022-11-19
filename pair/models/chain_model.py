import json
from web3 import Web3
from pydantic import BaseModel


class Chain(BaseModel):
    chainId: int

    @staticmethod
    def supported_chains():
        return [250, 1, 3, 4, 5, 10, 42, 137, 42161, 42220, 80001]

    @property
    def url(self):
        with open("utils/chains.json") as f:
            chains = json.load(f)
            return chains[str(self.chainId)]["apiEndpoint"]

    @property
    def api_keys(self):
        with open("utils/chains.json") as f:
            chains = json.load(f)
            return chains[str(self.chainId)]["apiKeys"]

    @property
    def w3(self):
        with open("utils/chains.json") as f:
            chains = json.load(f)
            rpc = chains[str(self.chainId)]["defaultRpcUrl"]
        return Web3(Web3.HTTPProvider(rpc))

    @property
    def mongo_client(self):
        raise NotImplementedError
