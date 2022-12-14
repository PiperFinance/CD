from tokens import providers, fixture, utils
from pair import pairs


all_pairs = pairs.fetch_all_pairs()

black_list = set()
providers.fetch_tokens(
    "tokens/providers.url.json",
    "tokens/providers"
)

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
        avoid_addresses={
            *black_list,
            *{pair.detail.address for pair in all_pairs.values()}

        }

    )
