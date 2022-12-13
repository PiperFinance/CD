import os
import pymongo

global _CLIENT
_CLIENT = None

MONGO_URL = os.getenv("MONGO_URL") or "mongodb://localhost:27018/"


def client(
    class_name: str,
    chain_id: int
):
    global _CLIENT
    if not _CLIENT:
        _CLIENT = pymongo.MongoClient(MONGO_URL)

    db = _CLIENT[str(chain_id)]
    col = db[class_name]
    return col
