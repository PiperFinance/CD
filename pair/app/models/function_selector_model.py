from enum import Enum
from web3 import Web3
from pydantic import BaseModel
from typing import List, Optional, NamedTuple

from configs.mongo_config import function_selector_client
from utils.types import HexStr


class ArgType(Enum):
    ADDRESS = "address"
    INT = "uint256"

    def parse(self, val):
        match self:
            case self.ADDRESS:
                return Web3.toChecksumAddress(f"0x{val[24:]}")
            case self.INT:
                return int(val, 16)
            case _:
                return val


class Arg(NamedTuple):
    title: str
    type: ArgType


class FunctionSelector(BaseModel):
    hex: HexStr
    text: str
    args: Optional[List[Arg]]

    @staticmethod
    def mongo_client():
        client = function_selector_client("FunctionSelector")
        client.create_index("hex", unique=True)
        return client
