from pydantic import BaseModel
from typing import List
from schema.py import Token


class ChainToken(BaseModel):
    chainId: int
    tokens: List[Token]
