from pymongo import MongoClient
from api.config import Config

client = MongoClient(Config.NOSQLDB_URI)
db = client[Config.NOSQLDB_NAME]
logs_collection = db[Config.LOGGING_COLLECTION_NAME]

class MongoDbService:
    @staticmethod
    def insert_log_entry(log_entry):
        logs_collection.insert_one(log_entry)
