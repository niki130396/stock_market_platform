# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import sys
from os import environ

import scrapy

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
from utils.db_tools import get_source_statement_types_map  # noqa E402


class FinancialStatementItem(scrapy.Item):
    data = scrapy.Field()
    income_statement = scrapy.Field()
    balance_sheet = scrapy.Field()
    cash_flow = scrapy.Field()

    def __init__(self):
        super().__init__()
        self.__statement_types_map = {
            v: k for k, v in get_source_statement_types_map().items()
        }

    def add_statement(self, statement_type, data):
        self[self.__statement_types_map[statement_type]] = data
