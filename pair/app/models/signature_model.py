from pydantic import BaseModel
from typing import List, Optional
from utils.types import HexStr


class Signature(BaseModel):
    hex: HexStr
    text: str
    args: Optional[List[str]]
