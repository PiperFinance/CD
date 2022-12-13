import requests
import json

url = "https://li.quest/v1/chains"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

with open("lifi-chains.json", "w+") as f:
    json.dump((chains := response.json().get('chains')), f)
    print(
        len(chains),
        {_['id']: _['key'] for _ in chains}
    )
