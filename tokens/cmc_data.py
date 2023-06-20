import requests, logging, json


skip, limit = 1, 5000
r = []
while True:
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        querystring = {
            "convert": "USD",
            "start": skip,
            "limit": limit,
            "aux": "platform,cmc_rank,max_supply,total_supply,tags,date_added",
        }
        headers = {"X-CMC_PRO_API_KEY": "7a4acc5d-f8d8-45e3-bf91-8231830dcfdc"}

        response = requests.request("GET", url, headers=headers, params=querystring)

        tokens = response.json().get("data", [])
        r = [*r, *tokens]
        print(f"{skip=} , {limit=} , {querystring=} , {len(tokens)=} , {len(r)=}")
        if len(tokens) < limit:
            break
        else:
            skip += limit
    except Exception as e:
        logging.exception(e)
        break


with open("res.json", "w+") as f:
    json.dump(r, f)


with_platforms = []
platforms = set()
non_tokens = []
for token in r:
    if token is not None and token.get("platform"):
        with_platforms.append(token)
        platforms.add(token.get("platform", {}).get("symbol"))

# NOTE - Platforms
# {'ETH', 'KLV', 'KLAY', 'FITFI', 'KAI', 'APT', 'XDC', 'OP', 'SX', 'HBAR', 'NULS', 'ONT', 'KAVA', 'AVAX', 'EGLD', 'BRISE', 'SOL', 'NEO', 'MATIC', 'ARB', 'STX', 'XOR', 'XRD', 'GLMR', 'ASTR', 'EOS', 'WAVES', 'ALGO', 'KCS', 'XLM', 'BCH', 'TRX', 'LUNA', 'HT', 'MOVR', 'BITCI', 'IOTX', 'FSN', 'NEAR', 'BTC', 'TBD', 'XEM', 'VLX', 'BNB', 'CHZ', 'JEWEL', 'DOGE', 'OKT', 'RBTC', 'WAN', 'BOBA', 'XTZ', 'PLS', 'ROSE', 'HTML', 'OSMO', 'SGB', 'FTM', 'TON', 'ONE', 'EVER', 'KAR', 'DOT', 'CRO', 'CANTO', 'ETC', 'ETHW', 'XRP', 'CELO', 'ATOM', 'LUNC', 'ELA', 'FUSE', 'AURORA', 'CORE', 'ZIL', 'TLOS', 'SUI', 'WEMIX', 'CFX', 'TOMO', 'METIS', 'VET', 'GNO', 'SCRT', 'ADA'}
# {
    # 'BITCI',
    # 'DOT', 'WAN', 'STX', 'XRD', 'XDC', 'BRISE', 'CRO', 'ROSE', 'OP', 'SUI', 'CHZ', 'ARBITRUM', 'CFX', 'VLX', 'PLS', 'BTC', 'EGLD', 'GNO', 'ETC', 'SOL', 'VET', 'ARB', 'MATIC', 'ATOM', 'KLAY', 'CELO', 'OSMO', 'TON', 'LUNA', 'ADA', 'NEAR', 'XEM', 'BCH', 'HTML', 'HT', 'WAVES', 'FSN', 'ONT', 'HBAR', 'ELA', 'XRP', 'ZIL', 'METIS', 'MOVR', 'APT', 'TRX', 'NULS', 'TBD', 'NEO', 'XOR', 'BOBA', 'KLV', 'ONE', 'AURORA', 'KAR', 'WEMIX', 'KAI', 'ETH', 'KAVA', 'OKT', 'FTM', 'FITFI', 'EVER', 'EOS', 'ASTR', 'TLOS', 'ETHW', 'RBTC', 'FUSE', 'ALGO', 'XLM', 'SCRT', 'DOGE', 'AVAX', 'SGB', 'CORE', 'CANTO', 'SX', 'TOMO', 'IOTX', 'XTZ', 'JEWEL', 'BNB', 'GLMR', 'LUNC', 'KCS'}

# NOTE - Converts
# USD,IRR,ETH,BTC


print(platforms, len(with_platforms))
