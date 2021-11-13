import os

from pymongo import MongoClient


class StockMarketDBConnector:
    HOST = os.environ.get("MONGO_HOST")
    USERNAME = os.environ.get("MONGO_USERNAME")
    PASSWORD = os.environ.get("MONGO_PASSWORD")
    PORT = 27017

    def __init__(self, collection):
        self.client = MongoClient(
            f"mongodb://{self.USERNAME}:{self.PASSWORD}@127.0.0.1:27017"
        )
        self.db = self.client.stock_market
        self.collection = eval(f"self.db.{collection}")

    def get_last_id(self):
        ids = [
            document["id"]
            for document in self.collection.find({}, {"id": 1, "_id": 0})
            .sort([("id", -1)])
            .limit(1)
        ]
        if not ids:
            return 1
        return ids[0] + 1

    def get_present_symbols(self):
        symbols = set(
            [
                document["symbol"]
                for document in self.collection.find({}, {"symbol": 1, "_id": 0})
            ]
        )
        return symbols
