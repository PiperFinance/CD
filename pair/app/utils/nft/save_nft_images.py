import requests
import base64
import re
import json
from typing import List, Dict
from mimetypes import guess_extension, guess_type

from models import Nft
from utils.types import Address, ChainId


def save_chain_nft_images(chain_id: ChainId):
    nfts = get_chain_nfts(chain_id)
    save_nft_images(nfts)


def get_chain_nfts(chain_id: ChainId):
    client = Nft.mongo_client(chain_id)
    nfts = list(client.find())
    if nfts not in [None, []]:
        return nfts


def save_nft_images(nfts: List[Dict]):
    for nft in nfts:
        if nft.get("uri"):
            save_nft_image(
                nft.get("address"),
                nft.get("id"),
                nft.get("uri")
            )


def decode_uri(uri: str):
    if uri[:5] == "https":
        return decode_https(uri)
    if uri[:4] == "ipfs":
        return decode_ipfs(uri)
    if uri[:4] == "data":
        return decode_base64(uri)


def decode_ipfs(uri: str):
    cid = uri.split(":")[1][2:]
    uri = f'https://ipfs.io/ipfs/{cid}'
    return decode_https(uri)


def decode_base64(uri: str):
    format = guess_extension(guess_type(uri)[0])

    if format == ".json":
        base64_data = re.sub('^data:application/.+;base64,', '', uri)

        base64_bytes = base64_data.encode('ascii')
        base64_bytes = base64.b64decode(base64_bytes)
        base64_json = json.loads(base64_bytes)
        uri = get_image_uri(base64_json)
        base_64 = decode_image_uri(uri)
        return decode_base64(base_64)

    else:
        # need_to_be_deleted = f'^data:{uri[5:10]}/.+;base64,'
        need_to_be_deleted = f'^{uri.split(",")[0]},'

        base64_data = re.sub(need_to_be_deleted, '', uri)

        return base64_data, format


def decode_https(uri: str):
    res = get_uri_json(uri)
    uri = get_image_uri(res)
    base_64 = decode_image_uri(uri)
    return decode_base64(base_64)


def get_uri_json(uri: str):
    res = requests.get(uri)
    res = res.json()
    return res


def get_image_uri(data: Dict):
    if data.get("image"):
        return data.get("image")
    for value in list(data.values()):
        value = str(value)
        if "https" in value or "ipfs" in value or "data" in value:
            return value


def decode_image_uri(uri: str):
    if uri[:5] == "https":
        base_64 = create_base64(uri)
    if uri[:4] == "ipfs":
        cid = uri.split(":")[1][2:]
        uri = f'https://ipfs.io/ipfs/{cid}'
        base_64 = create_base64(uri)
    if uri[:4] == "data":
        base_64 = uri

    return base_64


def create_base64(uri: str):
    res = requests.get(uri)
    base_64 = ("data:" +
               res.headers['Content-Type'] + ";" +
               "base64," + base64.b64encode(res.content).decode("utf-8"))
    return base_64


def write_image(
    address: Address,
    id: str,
    base_64: str,
    format: str
):

    path = f'nft_images/{address}_{id}{format}'

    btyes_data = base64.b64decode(base_64)

    with open(path, "wb") as f:
        f.write(btyes_data)


def save_nft_image(
    address: Address,
    id: str,
    uri: str
):
    base_64, format = decode_uri(uri)
    write_image(address, id, base_64, format)
