from pydantic import BaseModel
from typing import List, Optional


class Signature(BaseModel):
    hex: str
    text: str
    args: Optional[List[str]]
