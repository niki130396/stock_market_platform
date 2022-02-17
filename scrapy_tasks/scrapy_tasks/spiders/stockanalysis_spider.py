import sys
from os import environ

from scrapy.http import Request
from scrapy_tasks.base_spiders import FinancialStatementCrawlSpider  # noqa F401
from scrapy_tasks.items import FinancialStatementItem  # noqa F401

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
from utils.db_tools import (  # noqa E402
    NormalizedFieldsProcessor,
    get_company_id,
    get_next_unfetched_ticker,
    get_source_statement_types_map,
    map_normalized_field_to_field_id,
)


class StockAnalysisSpider(FinancialStatementCrawlSpider):
    name = "stock_analysis_spider"
    source_name = "stock_analysis"
    income_statement_source_definition = ("", "income_statement")
    balance_sheet_statement_source_definition = ("balance-sheet", "balance_sheet")
    cash_flow_statement_source_definition = ("cash-flow-statement", "cash_flow")

    def build_url(self, symbol: str, statement_type: str):
        url = f"https://stockanalysis.com/stocks/{symbol.lower()}/financials/"
        if statement_type:
            url += statement_type + "/"
        return url

    def start_requests(self):
        for obj in get_next_unfetched_ticker():

            for source_statement_type, local_statement_type in (
                self.income_statement_source_definition,
                self.balance_sheet_statement_source_definition,
                self.cash_flow_statement_source_definition,
            ):
                url = self.build_url(obj.symbol, source_statement_type)
                yield Request(
                    url=url,
                    callback=self.parse,
                    meta={"statement_type": local_statement_type, "document": obj},
                    headers={"Accept-Encoding": "gzip, deflate, utf-8"},
                )

    def parse(self, response, **kwargs):
        document = response.meta.get("document")  # noqa F841
        local_statement_type = response.meta.get("statement_type")

        rows = self.get_rows(response)

        normalized_rows = self.normalize_fields(rows, local_statement_type)
        item = FinancialStatementItem()
        item["metadata"] = response.meta.get("document")
        item["data"] = normalized_rows
        yield item

    def get_rows(self, response):
        years = self.get_years(response)
        parsed_rows = [years]
        table = response.xpath("//tbody//tr")

        if table:
            for row in table:
                elements = row.xpath("./td")
                row_values = []
                for el in elements:
                    value = el.xpath(".//span/text()[1]").get()
                    row_values.append(value)
                parsed_rows.append(row_values)

        return parsed_rows

    @staticmethod
    def get_years(response):
        output = []
        years = response.xpath("//thead//th")
        if years:
            element = years[0]
            value = element.xpath(".//span/text()[1]").get()
            if value:
                output.append(value)

            for element in years[1:]:
                value = element.xpath("./text()[1]").get()
                if value:
                    output.append(value)
        return output

    def normalize_fields(self, rows, statement_type):
        for row in rows[1:]:
            normalized_field = self.normalized_field_processor.get_local_field(
                statement_type, row[0]
            )
            row[0] = normalized_field
        return rows
