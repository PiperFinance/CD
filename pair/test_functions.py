
async def _tt_():
    from utils.pair.save_pairs import save_chain_pairs, save_chain_pairs_test
    from utils.transaction.save_transactions import save_users_chain_token_trxs
    from utils.nft.save_nfts import save_users_chain_nfts

    # save_chain_pairs(1)
    # save_chain_pairs_test(1)

    save_users_chain_token_trxs(
        250, "0x74D45069FfEB5547061F58b1307bd0c115f45446")

    save_users_chain_nfts(250, "0x614d9Ca71B7dC90dE2eb38938CF59DB1A4CE1372")

    pass
