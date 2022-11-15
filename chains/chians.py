INFURA_API_KEY = "1s7G4eZo0bBvuZlq8Cxqcsw7lgj"

# https://chainid.network/chains.json
DEFAULT_CHAIN_INFO = {
    1: {
        "name": "Ethereum Mainnet",
        "chain": "ETH",
        "icon": "ethereum",
        "rpc": [
            "https://mainnet.infura.io/v3/${INFURA_API_KEY}",
            "wss://mainnet.infura.io/ws/v3/${INFURA_API_KEY}",
            "https://api.mycryptoapi.com/eth",
            "https://cloudflare-eth.com",
        ],
        "faucets": [],
        "nativeCurrency": {"name": "Ether", "symbol": "ETH", "decimals": 18},
        "infoURL": "https://ethereum.org",
        "shortName": "eth",
        "chainId": 1,
        "networkId": 1,
        "slip44": 60,
        "ens": {"registry": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"},
        "explorers": [
            {
                "name": "etherscan",
                "url": "https://etherscan.io",
                "standard": "EIP3091",
            }
        ],
    },
    4: {
        "name": "Rinkeby",
        "title": "Ethereum Testnet Rinkeby",
        "chain": "ETH",
        "network": "testnet",
        "rpc": [
            "https://rinkeby.infura.io/v3/${INFURA_API_KEY}",
            "wss://rinkeby.infura.io/ws/v3/${INFURA_API_KEY}",
        ],
        "faucets": [
            "http://fauceth.komputing.org?chain=4&address=${ADDRESS}",
            "https://faucet.rinkeby.io",
        ],
        "nativeCurrency": {
            "name": "Rinkeby Ether",
            "symbol": "RIN",
            "decimals": 18,
        },
        "infoURL": "https://www.rinkeby.io",
        "shortName": "rin",
        "chainId": 4,
        "networkId": 4,
        "ens": {"registry": "0xe7410170f87102df0055eb195163a03b7f2bff4a"},
        "explorers": [
            {
                "name": "etherscan-rinkeby",
                "url": "https://rinkeby.etherscan.io",
                "standard": "EIP3091",
            }
        ],
    },
    5: {
        "name": "Görli",
        "title": "Ethereum Testnet Görli",
        "chain": "ETH",
        "network": "testnet",
        "rpc": [
            "https://goerli.infura.io/v3/${INFURA_API_KEY}",
            "wss://goerli.infura.io/v3/${INFURA_API_KEY}",
            "https://rpc.goerli.mudit.blog/",
        ],
        "faucets": [
            "http://fauceth.komputing.org?chain=5&address=${ADDRESS}",
            "https://goerli-faucet.slock.it?address=${ADDRESS}",
            "https://faucet.goerli.mudit.blog",
        ],
        "nativeCurrency": {"name": "Görli Ether", "symbol": "GOR", "decimals": 18},
        "infoURL": "https://goerli.net/#about",
        "shortName": "gor",
        "chainId": 5,
        "networkId": 5,
        "ens": {"registry": "0x112234455c3a32fd11230c42e7bccd4a84e02010"},
        "explorers": [
            {
                "name": "etherscan-goerli",
                "url": "https://goerli.etherscan.io",
                "standard": "EIP3091",
            }
        ],
    },
    10: {
        "name": "Optimism",
        "chain": "ETH",
        "rpc": ["https://mainnet.optimism.io/"],
        "faucets": [],
        "nativeCurrency": {"name": "Ether", "symbol": "ETH", "decimals": 18},
        "infoURL": "https://optimism.io",
        "shortName": "oeth",
        "chainId": 10,
        "networkId": 10,
        "explorers": [
            {
                "name": "etherscan",
                "url": "https://optimistic.etherscan.io",
                "standard": "EIP3091",
            }
        ],
    },
    42: {
        "name": "Kovan",
        "title": "Ethereum Testnet Kovan",
        "chain": "ETH",
        "network": "testnet",
        "rpc": [
            "https://kovan.poa.network",
            "http://kovan.poa.network:8545",
            "https://kovan.infura.io/v3/${INFURA_API_KEY}",
            "wss://kovan.infura.io/ws/v3/${INFURA_API_KEY}",
            "ws://kovan.poa.network:8546",
        ],
        "faucets": [
            "http://fauceth.komputing.org?chain=42&address=${ADDRESS}",
            "https://faucet.kovan.network",
            "https://gitter.im/kovan-testnet/faucet",
        ],
        "nativeCurrency": {"name": "Kovan Ether", "symbol": "KOV", "decimals": 18},
        "explorers": [
            {
                "name": "etherscan",
                "url": "https://kovan.etherscan.io",
                "standard": "EIP3091",
            }
        ],
        "infoURL": "https://kovan-testnet.github.io/website",
        "shortName": "kov",
        "chainId": 42,
        "networkId": 42,
    },
    56: {
        "name": "Binance Smart Chain Mainnet",
        "chain": "BSC",
        "rpc": [
            "https://bsc-dataseed1.binance.org",
            "https://bsc-dataseed2.binance.org",
            "https://bsc-dataseed3.binance.org",
            "https://bsc-dataseed4.binance.org",
            "https://bsc-dataseed1.defibit.io",
            "https://bsc-dataseed2.defibit.io",
            "https://bsc-dataseed3.defibit.io",
            "https://bsc-dataseed4.defibit.io",
            "https://bsc-dataseed1.ninicoin.io",
            "https://bsc-dataseed2.ninicoin.io",
            "https://bsc-dataseed3.ninicoin.io",
            "https://bsc-dataseed4.ninicoin.io",
            "wss://bsc-ws-node.nariox.org",
        ],
        "faucets": ["https://free-online-app.com/faucet-for-eth-evm-chains/"],
        "nativeCurrency": {
            "name": "Binance Chain Native Token",
            "symbol": "BNB",
            "decimals": 18,
        },
        "infoURL": "https://www.binance.org",
        "shortName": "bnb",
        "chainId": 56,
        "networkId": 56,
        "slip44": 714,
        "explorers": [
            {"name": "bscscan", "url": "https://bscscan.com", "standard": "EIP3091"}
        ],
    },
    100: {
        "name": "Gnosis Chain",
        "chain": "GNO",
        "icon": "gnosis",
        "rpc": [
            "https://rpc.gnosischain.com",
            "https://rpc.ankr.com/gnosis",
            "https://gnosischain-rpc.gateway.pokt.network",
            "https://gnosis-mainnet.public.blastapi.io",
            "wss://rpc.gnosischain.com/wss",
        ],
        "faucets": [
            "https://faucet.gimlu.com/gnosis",
            "https://stakely.io/faucet/gnosis-chain-xdai",
            "https://faucet.prussia.dev/xdai",
        ],
        "nativeCurrency": {"name": "xDAI", "symbol": "xDAI", "decimals": 18},
        "infoURL": "https://developers.gnosischain.com",
        "shortName": "gno",
        "chainId": 100,
        "networkId": 100,
        "slip44": 700,
        "explorers": [
            {
                "name": "blockscout",
                "url": "https://blockscout.com/xdai/mainnet",
                "icon": "blockscout",
                "standard": "EIP3091",
            }
        ],
    },
    128: {
        "name": "Huobi ECO Chain Mainnet",
        "chain": "Heco",
        "rpc": [
            "https://http-mainnet.hecochain.com",
            "wss://ws-mainnet.hecochain.com",
        ],
        "faucets": ["https://free-online-app.com/faucet-for-eth-evm-chains/"],
        "nativeCurrency": {
            "name": "Huobi ECO Chain Native Token",
            "symbol": "HT",
            "decimals": 18,
        },
        "infoURL": "https://www.hecochain.com",
        "shortName": "heco",
        "chainId": 128,
        "networkId": 128,
        "slip44": 1010,
        "explorers": [
            {
                "name": "hecoinfo",
                "url": "https://hecoinfo.com",
                "standard": "EIP3091",
            }
        ],
    },
    137: {
        "name": "Polygon Mainnet",
        "chain": "Polygon",
        "rpc": [
            "https://polygon-rpc.com/",
            "https://rpc-mainnet.matic.network",
            "https://matic-mainnet.chainstacklabs.com",
            "https://rpc-mainnet.maticvigil.com",
            "https://rpc-mainnet.matic.quiknode.pro",
            "https://matic-mainnet-full-rpc.bwarelabs.com",
        ],
        "faucets": [],
        "nativeCurrency": {"name": "MATIC", "symbol": "MATIC", "decimals": 18},
        "infoURL": "https://polygon.technology/",
        "shortName": "MATIC",
        "chainId": 137,
        "networkId": 137,
        "slip44": 966,
        "explorers": [
            {
                "name": "polygonscan",
                "url": "https://polygonscan.com",
                "standard": "EIP3091",
            }
        ],
    },
    250: {
        "name": "Fantom Opera",
        "chain": "FTM",
        "rpc": ["https://rpc.ftm.tools"],
        "faucets": ["https://free-online-app.com/faucet-for-eth-evm-chains/"],
        "nativeCurrency": {"name": "Fantom", "symbol": "FTM", "decimals": 18},
        "infoURL": "https://fantom.foundation",
        "shortName": "ftm",
        "chainId": 250,
        "networkId": 250,
        "icon": "fantom",
        "explorers": [
            {
                "name": "ftmscan",
                "url": "https://ftmscan.com",
                "icon": "ftmscan",
                "standard": "EIP3091",
            }
        ],
    },
    42161: {
        "name": "Arbitrum One",
        "chainId": 42161,
        "shortName": "arb1",
        "chain": "ETH",
        "networkId": 42161,
        "nativeCurrency": {"name": "Ether", "symbol": "ETH", "decimals": 18},
        "rpc": [
            "https://arbitrum-mainnet.infura.io/v3/${INFURA_API_KEY}",
            "https://arb-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}",
            "https://arb1.arbitrum.io/rpc",
        ],
        "faucets": [],
        "explorers": [
            {
                "name": "Arbiscan",
                "url": "https://arbiscan.io",
                "standard": "EIP3091",
            },
            {
                "name": "Arbitrum Explorer",
                "url": "https://explorer.arbitrum.io",
                "standard": "EIP3091",
            },
        ],
        "infoURL": "https://arbitrum.io",
        "parent": {
            "type": "L2",
            "chain": "eip155-1",
            "bridges": [{"url": "https://bridge.arbitrum.io"}],
        },
    },
    42220: {
        "name": "Celo Mainnet",
        "chainId": 42220,
        "shortName": "CELO",
        "chain": "CELO",
        "networkId": 42220,
        "nativeCurrency": {"name": "CELO", "symbol": "CELO", "decimals": 18},
        "rpc": ["https://forno.celo.org", "wss://forno.celo.org/ws"],
        "faucets": ["https://free-online-app.com/faucet-for-eth-evm-chains/"],
        "infoURL": "https://docs.celo.org/",
        "explorers": [
            {
                "name": "blockscout",
                "url": "https://explorer.celo.org",
                "standard": "none",
            }
        ],
    },
    43114: {
        "name": "Avalanche C-Chain",
        "chain": "AVAX",
        "rpc": ["https://api.avax.network/ext/bc/C/rpc"],
        "faucets": ["https://free-online-app.com/faucet-for-eth-evm-chains/"],
        "nativeCurrency": {"name": "Avalanche", "symbol": "AVAX", "decimals": 18},
        "infoURL": "https://www.avax.network/",
        "shortName": "Avalanche",
        "chainId": 43114,
        "networkId": 43114,
        "slip44": 9005,
        "explorers": [
            {
                "name": "snowtrace",
                "url": "https://snowtrace.io",
                "standard": "EIP3091",
            }
        ],
    },
    31337: {"rpc": ["http://127.0.0.1:8545/"]},
}


for chain_id, chain_info in DEFAULT_CHAIN_INFO.items():
    for rpc_index, rpc in enumerate(chain_info.get("rpc")):
        if "INFURA_API_KEY" in rpc:
            assert INFURA_API_KEY is not None, "Provide API KEY in Your Config"
            _: str = DEFAULT_CHAIN_INFO[chain_id]["rpc"][rpc_index]
            _ = _.replace("${INFURA_API_KEY}", INFURA_API_KEY)
            DEFAULT_CHAIN_INFO[chain_id]["rpc"][rpc_index] = _
            # string.Template("https://mainnet.infura.io/v3/${INFURA_API_KEY}").substitute(INFURA_API_KEY="asd")


CHAIN_SEPARATED_ADDRESS = {
    1: "0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441",
    4: "0x42Ad527de7d4e9d9d011aC45B31D8551f8Fe9821",
    5: "0x3b2A02F22fCbc872AF77674ceD303eb269a46ce3",
    10: "0x2DC0E2aa608532Da689e89e237dF582B783E552C",
    42: "0x2cc8688C5f75E365aaEEb4ea8D6a480405A48D2A",
    56: "0x1Ee38d535d541c55C9dae27B12edf090C608E6Fb",
    100: "0xb5b692a88BDFc81ca69dcB1d924f59f0413A602a",
    128: "0xc9a9F768ebD123A00B52e7A0E590df2e9E998707",
    137: "0xa1B2b503959aedD81512C37e9dce48164ec6a94d",
    250: "0xb828C456600857abd4ed6C32FAcc607bD0464F4F",
    42161: "0x269ff446d9892c9e19082564df3f5e8741e190a1",
    42220: "0x75F59534dd892c1f8a7B172D639FA854D529ada3",
    43114: "0x82979a6f8D628270B29F5687bEA2F73D5D0eC77d",
    31337: "0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441",
}

AGGREGATE_CALLS_FUNC = "aggregate3"  # "function aggregate3(Call3[] calldata calls) public payable (Result[] memory returnData)"
CHAIN_MULTI_CALL_V3 = "0xcA11bde05977b3631167028862bE2a173976CA11"
