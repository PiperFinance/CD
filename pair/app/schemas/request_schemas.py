from pydantic import BaseModel
from typing import List

from models import FunctionSelector
from utils.types import Address, ChainId, HexStr


# class GetPairs(BaseModel):
#     page_size: int
#     page_number: int


# class GetChainPairsLen(BaseModel):
#     chain_id: ChainId


# class GetChainPairs(BaseModel):
#     chain_id: ChainId
#     page_size: int
#     page_number: int


# class GetFunctionSelector(BaseModel):
#     hex: HexStr


# class GetFunctionSelectors(BaseModel):
#     hexs: List[HexStr]

class SaveFunctionSelector(BaseModel):
    function_selectors: FunctionSelector


class SaveFunctionSelectors(BaseModel):
    function_selectors: List[FunctionSelector]


# class GetUserDataLen(BaseModel):
#     user_address: Address


# class GetUserData(BaseModel):
#     user_address: Address
#     page_size: int
#     page_number: int


# class GetUserChainDataLen(BaseModel):
#     chain_id: ChainId
#     user_address: Address


# class GetUserChainData(BaseModel):
#     chain_id: ChainId
#     user_address: Address
#     page_size: int
#     page_number: int


# class GetUsersDataLen(BaseModel):
#     user_addresses: List[Address]


# class GetUsersData(BaseModel):
#     user_addresses: List[Address]
#     page_size: int
#     page_number: int


# class GetUsersChainDataLen(BaseModel):
#     chain_id: ChainId
#     user_addresses: List[Address]


# class GetUsersChainData(BaseModel):
#     chain_id: ChainId
#     user_addresses: List[Address]
#     page_size: int
#     page_number: int


class SaveUserData(BaseModel):
    userAddress: Address


class SaveUserChainData(BaseModel):
    chain_id: ChainId
    userAddress: Address


class SaveUsersData(BaseModel):
    userAddresses: List[Address]


class SaveUsersChainData(BaseModel):
    chain_id: ChainId
    userAddresses: List[Address]
