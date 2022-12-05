import logging
import requests
import json
import glob
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict
from pydantic import BaseModel
from tqdm import tqdm


from tokens import schema

logger = logging.getLogger(__name__)


def save_provider(provider_dir, provider):
    with open(os.path.join(provider_dir, f"{provider.name}.json"), "w+") as f:
        f.write(provider.json())


# @dataclass(init=True)
class Provider(BaseModel):
    name: str
    timestamp: str | datetime
    version: Optional[dict]
    keywords: list
    tags: dict
    logoURI: str
    tokens: List[schema.Token]

    @classmethod
    def load(cls, url, provider_dir, name=None):
        r = requests.get(url)
        if r.status_code == 200:
            try:
                res = r.json()
                if name is None:
                    name = res.get('name')
                    assert name, "No Value Found for name"
                if "tokens" in res.keys():
                    tokens = [_token
                              for token in res['tokens']
                              if (_token := schema.Token.load(token)) is not None
                              ]
                    provider = Provider(
                        name=name,
                        timestamp=datetime.now().isoformat(),
                        version=res.get("version", {}),
                        keywords=res.get("keywords", []),
                        tags=res.get("tags", {}),
                        logoURI=res.get("logoURI", ""),
                        tokens=tokens
                    )
                    return provider
            except json.JSONDecodeError:
                logger.error(f"Bad Request @ {name} :  { r.text}")
        else:
            logger.error(f"Bad Request @ {name} :  { r.text}")

        return None


class ViaProvider(Provider):
    @classmethod
    def load(cls, url, provider_dir, name=None):
        chains = requests.get(url).json()
        _r = []
        for chain_tokens in chains.values():
            for token in chain_tokens:
                chainId = int(token['chainId'])
                if chainId == 1666600000:
                    continue  # harmoni
                if chainId <= 0:
                    continue  # solana or etc.
                if token['address'] == "FvwEAhmxKfeiG8SnEvq42hc6whRyY3EFYAvebMqDNDGCgxN5Z":
                    continue  # coingecko
                if token['address'] == "0x":
                    continue  # coingecko
                if not token['address']:
                    continue  # clover ???
                _r.append(token)
        provider = Provider(**{
            "name": name,
            "timestamp": "2022-04-06T22:19:09+00:00",
            "version": {
                "major": 1,
                "minor": 0,
                "patch": 0
            },
            "keywords": [
                "default"
            ],
            "tags": {},
            "logoURI": "",
            "tokens": _r
        })

        return provider


class LiFiProvider(Provider):

    LIFI_SUPPORTED_CHAINS = {1: 'eth', 137: 'pol', 56: 'bsc', 100: 'dai', 250: 'ftm', 66: 'okt', 43114: 'ava', 42161: 'arb',
                             10: 'opt', 1285: 'mor', 1284: 'moo', 42220: 'cel', 122: 'fus', 25: 'cro', 106: 'vel', 1313161554: 'aur'}

    @classmethod
    def load(cls, url, provider_dir, name=None):
        if name is None:
            name = "LiFi"

        response = requests.get(url, headers={"accept": "application/json"})

        tokens: List[schema.Token] = []

        for chain, chain_tokens in response.json().get('tokens', {}).items():
            for _token in chain_tokens:
                token = schema.Token.load(_token)
                if token is not None:
                    tokens.append(token)
        provider = cls(
            name=name,
            timestamp=datetime.now().isoformat(),
            version={},
            keywords=[],
            tags={},
            logoURI="",
            tokens=tokens
        )

        return provider


CHAINS_WITH_MULTICALL: List[int] = [1, 42, 4, 5, 3, 11155111, 10, 69, 420, 42161, 421613, 421611, 137, 80001, 100, 43114, 43113, 4002, 250, 56, 97, 1284, 1285, 1287,
                                    1666600000, 25, 122, 19, 16, 114, 288, 1313161554, 592, 66, 128, 1088, 30, 31, 9001, 9000, 108, 18, 42262, 42220, 44787, 71402, 71401, 8217, 2001, 321, 106, 40]


class NativeTokensProvider(Provider):

    @classmethod
    def load(cls, url, provider_dir, name=None):
        tokens = [
            schema.Token(**{
                "providers": [
                    "NativeTokens"
                ],
                "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "chainId": chainId,
                "name": "Ether",
                "symbol": "ETH",
                "decimals": 18
            })
            for chainId in CHAINS_WITH_MULTICALL]

        return cls(
            name=name or "NativeTokens",
            timestamp=datetime.now().isoformat(),
            version={},
            keywords=["NativeTokens"],
            tags={},
            logoURI="",
            tokens=tokens
        )


def fetch_tokens(providers_url_file=None, provider_dir=None) -> Dict[str, Provider]:
    """
    For Providers that follow uniswap schema
    Attention:
     - Reads from  PROVIDER_URL_FILE
     - Writes Json Files to PROVIDER_DIR
    """
    if provider_dir is None:
        provider_dir = os.getenv('PROVIDER_DIR', 'providers')
    if providers_url_file is None:
        providers_url_file = os.getenv('PROVIDER_URL_FILE', 'providers')
    providers = {}
    with open(providers_url_file, 'r') as f:
        for provider, url in tqdm(json.load(f).items()):
            try:
                match provider:
                    case "ViaAll":
                        providers[provider] = ViaProvider.load(
                            url, provider_dir, provider)
                    case "Via":
                        providers[provider] = ViaProvider.load(
                            url, provider_dir, provider)
                    case "LiFi":
                        providers[provider] = LiFiProvider.load(
                            url, provider_dir, provider)
                    case "Natives":
                        providers[provider] = NativeTokensProvider.load(
                            url, provider_dir, provider)
                    case _:
                        providers[provider] = Provider.load(
                            url, provider_dir, provider)
                if providers[provider] is not None:
                    save_provider(provider_dir, providers[provider])
            except requests.exceptions.RequestException as e:
                logger.warning(f"ProviderLoader: Error {e}  @ {provider}")

    return providers


def get_fetched_providers(search_dir=None) -> Dict[str, Provider]:
    """
    Searches for provider json files in
    - arg: search_dir 
    - env: PROVIDER_DIR 

    """
    if search_dir is None:
        search_dir = os.environ['PROVIDER_DIR']
    providers = {}
    for file in glob.glob(os.path.join(search_dir, "*.json")):
        with open(file) as f:
            # with open(os.path.join(search_dir, file)) as f:
            provider_name = file.replace(".json", "").split(
                "\\" if os.name == 'nt' else "/")[-1]
            providers[provider_name] = Provider(**json.load(f))
    return providers


if __name__ == "__main__":
    fetch_tokens(
        "tokens/providers.url.json",
        "tokens/providers"
    )
