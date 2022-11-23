from typing import List

from .signature import get_signature


def decode_trx_input_data(input: str) -> List:

    func_selector = get_signature(input[:10])
    if func_selector in [[], None]:
        return

    func_signature = [func_selector]



    for i in range(11, len(input), 64):
        func_signature.append(input[i: i + 64])
    
    return func_signature
