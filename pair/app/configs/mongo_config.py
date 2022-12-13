import os
import pymongo
from utils.types import ChainId, Collation
global _CLIENT
_CLIENT = None

MONGO_URL = os.getenv("MONGO_URL") or "mongodb://localhost:27017/"


def client(
    class_name: str,
    chain_id: int | ChainId
) -> Collation:
    global _CLIENT
    if not _CLIENT:
        _CLIENT = pymongo.MongoClient(MONGO_URL)

    db = _CLIENT[str(chain_id)]
    col = db[class_name]
    return col


def function_selector_client(
    class_name: str
):
    global _CLIENT
    if not _CLIENT:
        _CLIENT = pymongo.MongoClient(MONGO_URL)

    db = _CLIENT[class_name]
    col = db[class_name]
    return col

# def client(
#     db_name: str,
#     chain_id: int
# ) -> AIOEngine:

#     _database_name = f"{chain_id}:{db_name}"

#     global _CLIENT, _ENGINES
#     if not _CLIENT:
#         _CLIENT = AsyncIOMotorClient("mongodb://localhost:27017")
#     if _database_name not in _ENGINES.keys():
#         _ENGINES[_database_name] = AIOEngine(
#             # motor_client=_CLIENT,
#             database=_database_name
#         )

#     return _ENGINES[_database_name]
