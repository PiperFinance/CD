from pydantic import BaseModel
from typing import Optional, List, Set
from zlib import crc32
import logging

logger = logging.getLogger(__name__)


class TokenDetail(BaseModel):
    chainId: int
    address: str
    name: str
    symbol: str
    decimals: int
    tags: Optional[List[str]]
    coingeckoId: Optional[str]
    lifiId: Optional[str]
    listedIn: Optional[List[str]]
    logoURI: Optional[str]
    verify: bool = False

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash("-".join([self.address.lower(), str(self.chainId)]))

    @property
    def checksum(self) -> int:
        return crc32("-".join([self.address.lower(), str(self.chainId)]).encode())


class Token(BaseModel):
    token: TokenDetail
    priceUSD: Optional[str] = None  # Later convert to float
    balance: Optional[str] = "0"
    value: Optional[str] = "0"
