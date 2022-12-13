from __future__ import annotations
from zlib import crc32
from typing import List, Dict, Optional

from pydantic import BaseModel

from schema.py import Token


class PairDetail(BaseModel):
    tokens: Dict[int, Token]
    tokensOrder: List[int]
    decimals: int
    chainId: int
    address: str
    symbol: str
    name: str
    dex: str
    verified: bool = False
    coingeckoId: Optional[str] = None

    @property
    def checksum(self) -> int:
        return crc32("-".join([self.address.lower(), str(self.chainId)]).encode())


class Pair(BaseModel):
    pair: PairDetail
    # pair related
    reserves: Optional[List[int]] = None
    totalSupply: Optional[str] = None
    priceUSD: Optional[float] = None
    # User related
    balance: Optional[int] = None
    value: Optional[float] = None
