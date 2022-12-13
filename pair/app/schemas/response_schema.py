from typing import List, Optional, Any
from pydantic import BaseModel

from models import Trx, Nft, FunctionSelector, Pair


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class PairList(BaseResponse):
    result: Optional[List[Pair]]


class NftList(BaseResponse):
    result: Optional[List[Nft]]


class TrxList(BaseResponse):
    result: Optional[List[Trx]]


class FunctionSelectorList(BaseResponse):
    result: Optional[List[FunctionSelector]]

class FunctionSelectorResponse(BaseResponse):
    result: Optional[FunctionSelector]
