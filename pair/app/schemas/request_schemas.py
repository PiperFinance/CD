from pydantic import BaseModel
from typing import List

from models import FunctionSelector
from utils.types import Address, ChainId


class SaveFunctionSelector(BaseModel):
    function_selectors: FunctionSelector


class SaveFunctionSelectors(BaseModel):
    function_selectors: List[FunctionSelector]


class SaveUserData(BaseModel):
    userAddress: Address


class SaveUserChainData(BaseModel):
    chainId: ChainId
    userAddress: Address


class SaveUsersData(BaseModel):
    userAddresses: List[Address]


class SaveUsersChainData(BaseModel):
    chainId: ChainId
    userAddresses: List[Address]
