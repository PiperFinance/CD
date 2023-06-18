from typing import Optional
import logging
import requests
from web3.exceptions import ContractLogicError
from tqdm import tqdm
from web3 import Web3


from schema import py as schema

from tokens.utils import _CONTRACTS
from tokens.providers import get_fetched_providers, save_provider

logger = logging.getLogger(__name__)

_cache = {}
_failed_chains = []


def fix_providers(provider_dir, save=True, fix_symbol=True, fix_address=True):
    providers = get_fetched_providers(provider_dir)
    for provider_name, provider in providers.items():
        _res_tokens = []
        _bad_tokens = []
        print(f"\nProvider: {provider_name}")
        for i, token in tqdm(enumerate(provider.tokens)):
            if fix_address:
                token = fix_token_address(token)
            if token is not None and fix_symbol:
                token = fix_token_symbol(token)
            if token is not None:
                _res_tokens.append(token)
            else:
                _bad_tokens.append(token)
        provider.tokens = _res_tokens
        if save:
            save_provider(provider_dir, provider)


def _token_key(token: schema.TokenDetail):
    return (token.address, token.chainId)


def fix_token_symbol(token: schema.TokenDetail, provider: Optional[str] = None) -> Optional[schema.TokenDetail]:
    """Calls Contracts address via web3 clients

    Arguments:
        token -- token object

    Keyword Arguments:
        provider -- provider listed this token 

    Returns:
        Returns None if sure token is self-destructed other vise tries fixes token 
    """
    token_key = _token_key(token)
    if token.chainId in _failed_chains:
        return token
    try:
        old_symbol = token.symbol

        # Usage of cache
        if token_key not in _cache:
            _cache[token_key] = _CONTRACTS[token.chainId](
                token.address).functions.symbol().call()

        # Cache Old symbol
        if provider:
            token.listedIn = [*(token.listedIn or []), provider]

        token.symbol = _cache[token_key]

        # NOTE - Token has bad symbol
        if old_symbol != token.symbol:
            logger.warning(
                f"  old:{old_symbol}, new:{token.symbol} \t {token}")

    except ContractLogicError as e:
        logger.warning(f" --- Error {e} @ {token_key or token.address}")
        return None

    except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        _failed_chains.append(token.chainId)
        logger.warning(
            f"  --- Error {e} @ {token_key} rpc :  {_CONTRACTS[token.chainId](token.address).web3.provider}")
        return token

    except Exception as e:
        if "to C ssize_t" in str(e):
            return token
        else:
            logger.warning(f"  --- Error {e} @{token_key}")
            return None

    return token


def fix_token_address(token: schema.TokenDetail) -> Optional[schema.TokenDetail]:
    _add = token.address
    match _add:
        case "0xaa44051bdd76e251aab66dbbe82a97343b4d7da3#code":
            _add = '0xaa44051bdd76e251aab66dbbe82a97343b4d7da3'
        case "0x77F86D401e067365dD911271530B0c90DeC3e0f7/":
            _add = "0x77F86D401e067365dD911271530B0c90DeC3e0f7"
        case "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2#balances":
            _add = "0x06ae7A979D9818B64498c8acaFDd0ccc78bC6fd2"
        case "0x0000000000000000000000000000000000000000":
            _add = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    try:
        try:
            token.address = Web3.toChecksumAddress(_add)
        except AttributeError:
            token.address = Web3.to_checksum_address(_add)
            
    except Exception as e:
        logger.warning(f"   --- Bad Address Error {e} @ {_token_key(token)}")
        return None

    return token
