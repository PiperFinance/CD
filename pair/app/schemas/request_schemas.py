from pydantic import BaseModel
from typing import List

from utils.types import Address, ChainId


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
