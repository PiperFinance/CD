import json
import requests

RAW_CHAINS_URL = "https://chainid.network/chains.json"

with open("raw-chains.json", "w+") as f:
    json.dump(requests.get(RAW_CHAINS_URL).json(), f)

with (
    open("raw-chains.json", "r") as r_f,
    open("main-net-chains.json", "w+") as main_f,
    open("testnet-chains.json", "w+") as test_f
):
    chains = json.load(r_f)
    main_net = []
    test_net = []
    for chain in chains:
        for word in ["testnet", "test", "ropsten", "rinkby", "kovan", "test-net", "testy", "test net", "net-test"]:
            if word in str(chain).lower():
                test_net.append(chain)
            else:
                main_net.append(chain)
    json.dump(main_net, main_f)
    json.dump(test_net, test_f)
