# from tokens import providers, fixture, utils

# # providers.fetch_tokens(
# #     "tokens/providers.url.json",
# #     "tokens/providers"
# # )


# fixture.fix_providers("tokens/providers", fix_symbol=False)


# with open("tokens/README.md", "w+") as f:
#     utils.provider_data_merger(providers.get_fetched_providers(
#         "tokens/providers"), "tokens/outVerified/", True, try_request_token_logo=False, result_readme_file=f)

from pair import pairs
pairs.main()
