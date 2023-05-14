from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class NativeCurrency(BaseModel):
    name: str
    symbol: str
    decimals: int


class RpcUrls(BaseModel):
    infura: Optional[str] = None
    default: str
    public: str
    alchemy: Optional[str] = None


class Ens(BaseModel):
    address: str


class Multicall(BaseModel):
    address: str
    blockCreated: int


class Default(BaseModel):
    name: str
    url: str


class Public(BaseModel):
    name: str
    url: str


class BlockExplorers(BaseModel):
    default: Default
    public: Public


class Chain(BaseModel):
    nativeCurrency: NativeCurrency
    chainId: int = Field(0, alias="id")
    name: str
    network: str
    rpc: List[str]
    rpcUrls: RpcUrls
    ens: Optional[Ens] = None
    multicall: Optional[Multicall] = None
    blockExplorers: Optional[BlockExplorers] = None
    testnet: bool
