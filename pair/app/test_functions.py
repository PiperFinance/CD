
async def _tt_():
    from utils.pair.save_pairs import save_chain_pairs, save_all_pairs
    from utils.pair.update_pairs import update_chain_pairs, update_all_pairs
    from utils.pair.get_pairs import get_chain_pairs, get_all_pairs
    from utils.transaction.save_transactions import save_user_chain_token_trxs, save_user_all_token_trxs
    from utils.transaction.get_transactions import get_user_chain_token_trxs, get_user_all_token_trxs
    from utils.nft.save_nfts import save_user_chain_nfts, save_user_all_nfts
    from utils.nft.get_nfts import get_user_chain_nfts, get_user_all_nfts
    from utils.transaction.four_bytes_function_selector import save_all_4bytes_function_selectors

    skip = 0
    limit = 5

    # save_chain_pairs(250)
    # save_all_pairs()

    # update_chain_pairs(250)
    # update_all_pairs()

    # get_chain_pairs(250, skip, limit)
    # get_all_pairs(skip, limit)

    # save_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5")
    
    # save_user_chain_token_trxs(
    #     1, "0x7d1F235a2eD3f71143c7eD0f5CB1A40b5b5d1aa6")

    # save_user_all_token_trxs("0x416299AAde6443e6F6e8ab67126e65a7F606eeF5")

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 5, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 10, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 15, limit)
    # get_user_all_token_trxs(
    #     "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip, limit)

    # save_user_chain_nfts(1, "0x76E44E267fD6E0189D71d38A257404C59A1Eb677")
    # save_user_all_nfts("0x76E44E267fD6E0189D71d38A257404C59A1Eb677")

    # get_user_chain_nfts(
    #     1, "0x76E44E267fD6E0189D71d38A257404C59A1Eb677", skip, limit)
    # get_user_chain_nfts(
    #     1, "0x76E44E267fD6E0189D71d38A257404C59A1Eb677", skip + 5, limit)
    # get_user_chain_nfts(
    #     1, "0x76E44E267fD6E0189D71d38A257404C59A1Eb677", skip + 10, limit)
    # get_user_all_nfts(
    #     "0x76E44E267fD6E0189D71d38A257404C59A1Eb677", skip, limit)

    # save_all_4bytes_signatures()

    pass
