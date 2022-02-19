import sys
from os import environ

from scrapy.http import Request
from scrapy_tasks.base_spiders import FinancialStatementCrawlSpider  # noqa F401
from scrapy_tasks.items import FinancialStatementItem  # noqa F401

sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
from utils.common import parse_numeric_string  # noqa E402
from utils.db_tools import get_next_unfetched_ticker  # noqa E402


class StockAnalysisSpider(FinancialStatementCrawlSpider):
    name = "stock_analysis_spider"
    source_name = "stock_analysis"
    income_statement_source_definition = ("", "income_statement")
    balance_sheet_statement_source_definition = ("balance-sheet", "balance_sheet")
    cash_flow_statement_source_definition = ("cash-flow-statement", "cash_flow")

    @staticmethod
    def build_url(symbol: str, statement_type: str):
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

        rows = self.get_rows(response, local_statement_type)
        rows_to_insert = self.arrange_rows_for_insertion(rows, document)

        item = FinancialStatementItem()
        item["metadata"] = response.meta.get("document").__dict__
        item["metadata"]["statement_type"] = local_statement_type
        item["data"] = rows_to_insert
        yield item

    def get_rows(self, response, statement_type):
        years = self.get_years(response)
        parsed_rows = [years]
        table = response.xpath("//tbody//tr")

        if table:
            for row in table:
                elements = row.xpath("./td")
                row_values = []
                row_name = elements[0].xpath(".//span/text()[1]").get()

                normalized_row_name = self.normalized_field_processor.get_local_field(
                    statement_type, row_name
                )
                if not normalized_row_name:
                    continue

                row_values.append(normalized_row_name)
                for el in elements[1:]:
                    value = el.xpath(".//span/text()[1]").get()
                    row_values.append(parse_numeric_string(value))

                while row_values[-1] is None or isinstance(row_values[-1], str):
                    row_values.pop()

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
                    output.append(parse_numeric_string(value))
        return output

    def arrange_rows_for_insertion(self, rows, document):
        output = []
        for i in range(1, len(rows[0])):
            period = rows[0][i]
            for row in rows[1:]:
                field_id = self.normalized_field_processor.get_normalized_field_id(
                    row[0]
                )
                try:
                    value = row[i]
                except IndexError:
                    continue
                output.append((document.id, field_id, period, value))
        return output
