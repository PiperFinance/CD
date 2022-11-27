from models import Chain, Pair


def get_all_pairs():
    pairs = []
    for chain_id in Chain.supported_chains():
        pairs.extend(get_chain_pairs(chain_id))


def get_chain_pairs(chain_id: int):
    client = Pair.mongo_client(chain_id)
    return client.find()
