
from src.config import config

if config.mongodb_conn is not None:
    from pymongo import MongoClient
    mongo_client = MongoClient(config.mongodb_conn)
    mongo_db = mongo_client['finbot']
else:
    # TODO pymongolite
    pass