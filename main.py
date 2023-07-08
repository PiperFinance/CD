from logging import getLogger
from chains import main
from schema.py.Token import TokenDetail
from tokens import providers, fixture, utils
from pair import pairs

logger = getLogger(__name__)

# try:
#     all_chains = main.fetch_all_chains()
# except Exception as e:
#     logger.exception(e)

try:
    ## TODO - NEEDS Refactor ... !
    all_pairs = pairs.fetch_all_pairs()
except Exception as e:
    all_pairs = {}
    logger.exception(e)


def late_night_fixes(token_det: TokenDetail):
    if token_det.checksum == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee-100":
        token_det.coingeckoId = "xdai"
    return token_det


try:
    black_list = set()
    providers.fetch_tokens("tokens/providers.url.json", "tokens/providers")
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
                *{pair.detail.address for pair in all_pairs.values()},
            },
            late_night_fixes=late_night_fixes,
        )
except Exception as e:
    logger.exception(e)
