from typing import List, Optional, Any
from pydantic import BaseModel

from models import Pair


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class PairList(BaseResponse):
    result: Optional[List[Pair]]
