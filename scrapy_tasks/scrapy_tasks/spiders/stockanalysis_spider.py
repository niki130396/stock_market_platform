import sys
from os import environ

from scrapy.http import Request
from scrapy.spiders import CrawlSpider

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
from utils.db_tools import (  # noqa E402
    NormalizedFieldsProcessor,
    get_company_id,
    get_next_unfetched_ticker,
    get_source_statement_types_map,
    map_normalized_field_to_field_id,
)


class StockAnalysisSpider(CrawlSpider):
    name = "stock_analysis_spider"

    def __init__(self):
        super().__init__()
        self.source_name = "stock_analysis"

    def build_url(self, symbol: str, statement_type: str):
        url = f"https://stockanalysis.com/stocks/{symbol.lower()}/financials/"
        if statement_type:
            url += statement_type + "/"
        return url

    def start_requests(self):
        fields_processor = NormalizedFieldsProcessor(self.source_name)

        for obj in get_next_unfetched_ticker():

            for statement_type in ("", "balance-sheet", "cash-flow-statement"):
                url = self.build_url(obj.symbol, statement_type)
                yield Request(
                    url=url,
                    callback=self.parse,
                    meta={"statement_type": statement_type, "document": obj},
                    headers={"Accept-Encoding": "gzip, deflate, utf-8"},
                )

    def parse(self, response, **kwargs):
        rows = self.get_rows(response)
        return rows

    def get_rows(self, response):
        table = response.xpath("//tbody//tr")
        parsed_rows = []

        if table:
            for row in table:
                elements = row.xpath("./td")
                row_values = []
                for el in elements:
                    value = el.xpath(".//span/text()[1]").get()
                    row_values.append(value)
                parsed_rows.append(row_values)
        return parsed_rows

    def extract_elements_by_column(self, rows: list, statement_type):
        if rows:
            container = []
            for column in range(1, len(rows[0])):
                period = rows[0][column]
                rows_by_period = {"period": period}
                for row in rows[1:]:
                    if row[0] in self.normalized_fields[statement_type]:
                        local_field = self.normalized_fields[statement_type][row[0]]
                        rows_by_period.update({local_field: row[column]})
                container.append(rows_by_period)
        return container
