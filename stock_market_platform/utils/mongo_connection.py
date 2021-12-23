from django.conf import settings
from pymongo import MongoClient


class StockMarketDBConnector:
    def __init__(self, collection):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client.stock_market
        if hasattr(self.db, collection):
            self.collection = getattr(self.db, collection)
        else:
            raise AttributeError(
                "The requested collection does not exist in the stock_market database"
            )

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
