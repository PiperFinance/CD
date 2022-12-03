from pydantic import BaseModel
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


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

    @classmethod
    def load(cls, token: dict):
        try:
            if "coinkey" in token:
                token['lifiId'] = token.pop('coinkey')
            return cls(**token)
        except Exception as tokenLoadError:
            logger.error(f"{tokenLoadError=} @ t_a :{token.get('address')}")
