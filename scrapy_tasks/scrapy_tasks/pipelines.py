# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from utils.db_tools import update_ticker_status, update_statement_type_availability  # noqa F402


class FinancialStatementPipeline:
    collection_name = "financial_statements"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.current_symbol = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB_NAME"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = dict(item)

        self.db[self.collection_name].insert(item)
        update_statement_type_availability(
            item["metadata"]["statement_type"],
            item["metadata"]["symbol"]
        )
        update_ticker_status(item["metadata"]["symbol"])
        return item
