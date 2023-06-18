from pydantic import BaseModel
from typing import Optional, List, Set
import logging

logger = logging.getLogger(__name__)


class TokenDetail(BaseModel):
    chainId: int
    address: str
    name: str
    symbol: str
    decimals: int = -1
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
    def checksum(self) -> str:
        return "-".join([self.address.lower(), str(self.chainId)])


class Token(BaseModel):
    detail: TokenDetail
    priceUSD: Optional[str] = None  # Later convert to float
    balance: Optional[str] = "0"
    value: Optional[str] = "0"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash("-".join([self.detail.address.lower(), str(self.detail.chainId)]))
