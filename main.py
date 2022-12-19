import json
from tokens import providers, fixture, utils
from pair import pairs


all_pairs = pairs.fetch_all_pairs()

black_list = set()
providers.fetch_tokens(
    "tokens/providers.url.json",
    "tokens/providers"
)

try:
    with open("tokens/block_list.json") as f:
        black_list.update([id for id in json.load(f)])
finally:
    black_list.update([pair_id for pair_id in all_pairs.keys()])
    ...
print(f"avoiding {len(black_list)} pairs ...")

fixture.fix_providers("tokens/providers", fix_symbol=False)
with open("tokens/README.md", "w+") as f:
    utils.provider_data_merger(
        providers.get_fetched_providers("tokens/providers"),
        "tokens/outVerified/",
        verify=True,
        include_testnet=False,
        find_logo_in_cache=True,
        try_request_token_logo=False,
        token_logoURI_BaseURL="https://raw.githubusercontent.com/PiperFinance/LO/main/logo",
        result_readme_file=f,
        black_list=black_list,
        avoid_self_destructed_contracts=True

    )
