# import time
#
# from airflow.models import DAG
# from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from utils.db_tools import (  # noqa E402
#     NormalizedFieldsProcessor,
#     get_company_id,
#     get_next_unfetched_ticker,
#     get_source_statement_types_map,
#     map_normalized_field_to_field_id,
# )
# from utils.models import DocumentModel
# from utils.selenium_helpers import element_exists  # noqa E402
#
# SOURCE_NAME = "yahoo_finance"
#
#
# class YahooStatementDataClass:
#     def __init__(self, metadata: DocumentModel):
#         self.metadata = metadata
#
#     def set_statement_type(self, statement_type):
#         setattr(self.metadata, "statement_type", statement_type)
#
#
# with DAG(
#     "yahoo_statements_dag",
#     start_date=days_ago(1),
#     schedule_interval=None,
#     max_active_runs=1,
# ) as yahoo_statements_dag:
#
#     def connect_browser():
#         options = webdriver.ChromeOptions()
#         options.add_argument("--no-sandbox")
#         driver = webdriver.Remote(
#             "http://stock_market_selenium:4444/wd/hub", options=options
#         )
#         return driver
#
#     def get_rows(browser):
#         table = browser.find_elements(
#             by=By.XPATH, value="//div[contains(@class, 'D(tbr)')]"
#         )
#         parsed_rows = []
#         if table:
#             for row in table:
#                 element = row.find_elements(by=By.XPATH, value="./div")
#                 parsed_row = []
#                 for item in element:
#                     text = item.text
#                     if text:
#                         parsed_row.append(text)
#                     else:
#                         parsed_row.append(text)
#                 parsed_rows.append(parsed_row)
#         return parsed_rows
#
#     def extract_elements_by_column(rows: list, statement_type, normalized_fields):
#         container = []
#         for column in range(1, len(rows[0])):
#             period = rows[0][column]
#             rows_by_period = {"period": period}
#             for row in rows[1:]:
#                 if row[0] in normalized_fields[statement_type]:
#                     local_field = normalized_fields[statement_type][row[0]]
#                     rows_by_period.update({local_field: row[column]})
#             container.append(rows_by_period)
#         return container
#
#     def fetch_statements_from_yahoo():
#         browser = connect_browser()
#         fields_processor = NormalizedFieldsProcessor("yahoo_finance")
#         n_statements = 1
#
#         for company_object in get_next_unfetched_ticker():
#             symbol = company_object.symbol
#             for statement_type in ("financials", "balance-sheet", "cash-flow"):
#                 start_time = time.time()
#                 url = f"https://finance.yahoo.com/quote/{symbol}/{statement_type}?p={symbol}"
#                 print(url)
#
#                 statement_obj = YahooStatementDataClass(company_object)
#                 statement_obj.set_statement_type(statement_type)
#
#                 browser.get(url)
#                 if element_exists(browser, By.CSS_SELECTOR, "button.btn:nth-child(5)"):
#                     browser.execute_script(
#                         "document.getElementsByClassName('btn primary')[0].click()"
#                     )
#
#                 time.sleep(2)
#                 if element_exists(
#                     browser,
#                     By.XPATH,
#                     "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/button",
#                 ):
#                     browser.find_element(
#                         by=By.XPATH,
#                         value="/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/button",  # noqa E501
#                     ).click()
#
#                     rows = get_rows(browser)
#                     if rows:
#                         rearranged_rows = extract_elements_by_column(
#                             rows, statement_type, fields_processor.mapped_source_fields
#                         )
#                         setattr(statement_obj, "data", rearranged_rows)
#                         end_time = time.time()
#                         print(statement_obj.metadata.symbol)
#                         print(statement_obj.data)
#                         print(n_statements)
#                         print(end_time - start_time)
#                         n_statements += 1
#                     else:
#                         print("NO ROWS")
#                 else:
#                     print("NO ELEMENTS")
#
#             time.sleep(2)
#         browser.quit()
#
#     yahoo_statements_task = PythonOperator(
#         task_id="yahoo_statements_task", python_callable=fetch_statements_from_yahoo
#     )
