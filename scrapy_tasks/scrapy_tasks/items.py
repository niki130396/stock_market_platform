# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import sys
from os import environ

import scrapy

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")


class FinancialStatementItem(scrapy.Item):
    metadata = scrapy.Field()
    data = scrapy.Field()
