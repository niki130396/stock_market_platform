import sys
from os import environ

from scrapy.spiders import CrawlSpider

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
from utils.db_tools import (  # noqa E402
    NormalizedFieldsProcessor,
    get_company_id,
    get_next_unfetched_ticker,
    get_source_statement_types_map,
    map_normalized_field_to_field_id,
)


class FinancialStatementCrawlSpider(CrawlSpider):
    source_name = None
    income_statement_source_definition = None
    balance_sheet_statement_source_definition = None
    cash_flow_statement_source_definition = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.source_name:
            raise AttributeError(
                "Provide a source_name attribute in order to instantiate"
            )

        self.normalized_field_processor = NormalizedFieldsProcessor(self.source_name)
