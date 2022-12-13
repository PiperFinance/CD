import requests
dexs = requests.get(
    "https://raw.githubusercontent.com/PiperFinance/CD/main/dexs/address_book.json").json()
tokens = requests.get(
    "https://github.com/PiperFinance/CD/blob/main/tokens/outVerified/chain_separated.json?raw=true").json()


def get_pairs(dexs, tokens):
    return
