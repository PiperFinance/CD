from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    chainId: int
    address: str
    name: str
    symbol: str
    decimals: int
    priceUSD: Optional[str]  # Later convert to float
    tags: Optional[List[str]]
    coingeckoId: Optional[str]
    lifiId: Optional[str]  # ! In lifi list is coinkey
    listedIn: Optional[List[str]]
    logoURI: Optional[str]
