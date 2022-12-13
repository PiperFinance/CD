from web3.contract import Contract
from web3 import Web3
try:
    from pymongo import MongoClient
    from pymongo.collation import Collation
except ImportError:
    MongoClient = object()
    Collation = object()
