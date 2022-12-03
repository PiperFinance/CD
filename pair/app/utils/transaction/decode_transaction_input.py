from typing import List

from models import Label
from .four_bytes_function_selector import get_4bytes_single_function_selector
from .get_function_selectors import get_function_selector


def decode_trx_input_data(input: str) -> List[Label]:
    if input == "deprecated":
        return

    labels = []

    func_sig_with_args = get_function_selector(input[:11])

    if func_sig_with_args:
        labels.append(Label(**{
            "title": func_sig_with_args.hex,
            "value": func_sig_with_args.text
        }))

        starter = 11

        for arg in func_sig_with_args.args:
            labels.append(Label(**{
                "title": arg,
                "value": input[starter, starter + 64]
            }))
            starter += 64

        return labels

    func_sig = get_4bytes_single_function_selector(input[:11])

    if func_sig:
        return [(Label(**{
            "title": input[:11],
            "value": func_sig
        }))]
