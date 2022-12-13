import json
from pydantic import BaseConfig


class Constants(BaseConfig):
    chains: Dict[ChainId, Chain]


with open("utils/chains.json") as f:
    Constants.chains = json.load(f)

constants = Constants()