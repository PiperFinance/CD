import requests
import json
import schema
from typing import List

lifi_chains = {1: 'eth', 137: 'pol', 56: 'bsc', 100: 'dai', 250: 'ftm', 66: 'okt', 43114: 'ava', 42161: 'arb',
               10: 'opt', 1285: 'mor', 1284: 'moo', 42220: 'cel', 122: 'fus', 25: 'cro', 106: 'vel', 1313161554: 'aur'}


class LifiProvider:

    url = "https://li.quest/v1/tokens"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    all_tokens: List[schema.Token] = []

    for chain in response.json().get('tokens'):
        all_tokens.append(schema.Token())

    with open("lifi.json", "w+") as f:
        json.dump(response.json(), f)
