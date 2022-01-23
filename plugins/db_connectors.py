# from os import environ
#
# from pymongo import MongoClient
#
# MONGO_HOST = environ["MONGO_HOST"]
# MONGO_DB = environ["MONGO_DB"]
# MONGO_USER = environ["MONGO_USER"]
# MONGO_PASSWORD = environ["MONGO_PASSWORD"]
# MONGO_PORT = environ["MONGO_PORT"]
#
# MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
#
#
# class StockMarketDBConnector:
#     COLLECTION = None
#
#     def __init__(self):
#         self.client = MongoClient(MONGO_URI)
#         self.db = self.client.stock_market
#         if getattr(self, "COLLECTION"):
#             self.collection = eval(f"self.db.{self.COLLECTION}")
#         else:
#             raise AttributeError("Please provide a collection to work with")
#
#     def get_last_id(self):
#         ids = [
#             document["id"]
#             for document in self.collection.find({}, {"id": 1, "_id": 0})
#             .sort([("id", -1)])
#             .limit(1)
#         ]
#         if not ids:
#             return 1
#         return ids[0] + 1
#
#     def get_present_symbols(self):
#         symbols = set(
#             [
#                 document["symbol"]
#                 for document in self.collection.find({}, {"symbol": 1, "_id": 0})
#             ]
#         )
#         return symbols
