from pydantic import BaseModel
from typing import List, Optional

from configs.mongo_config import function_selector_client
from utils.types import HexStr


class FunctionSelector(BaseModel):
    hex: HexStr
    text: str
    args: Optional[List[str]]

    @staticmethod
    def mongo_client():
        client = function_selector_client("FunctionSelector")
        client.create_index("hex", unique = True)
        return client
