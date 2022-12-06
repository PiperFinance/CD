from tokens import providers, fixture, utils

providers.fetch_tokens(
    "tokens/providers.url.json",
    "tokens/providers"
)

fixture.fix_providers("tokens/providers")


utils.provider_data_merger(providers.get_fetched_providers(
    "tokens/providers"), "tokens/outVerified/", True)
