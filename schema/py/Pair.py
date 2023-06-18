from __future__ import annotations
from typing import List, Dict, Optional

from pydantic import BaseModel

from schema.py import Token


class PairDetail(BaseModel):
    tokens: Dict[str, Token]
    tokensOrder: List[str]
    decimals: int
    chainId: int
    address: str
    symbol: str
    name: str
    dex: str
    verified: bool = False
    coingeckoId: Optional[str] = None

    @property
    def checksum(self) -> str:
        return "-".join([self.address.lower(), str(self.chainId)])


class Pair(BaseModel):
    detail: PairDetail
    # pair related
    reserves: Optional[List[int]] = None
    totalSupply: Optional[str] = None
    priceUSD: Optional[float] = None
    # User related
    balance: Optional[int] = None
    value: Optional[float] = None
