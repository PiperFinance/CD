from typing import List

from models import Signature
from ..sync_redis import (
    cache_func_sig_with_args,
    get_func_sig_with_args_from_redis
)
from utils.types import HexStr


def save_signatures(signatures: List[Signature]):
    for signature in signatures:
        cache_func_sig_with_args(
            signature.hex,
            signature
        )


def get_signatures(hexs: List[HexStr]) -> List[Signature]:
    signatures = []

    for hex in hexs:
        signature = get_func_sig_with_args_from_redis(hex)
        if signature:
            signatures.append(signature)

    return signatures
