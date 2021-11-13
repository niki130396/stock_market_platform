# from os import environ
#
# import psycopg2
# import requests
# from airflow.models import DAG
# from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago
# from db_connectors import StockMarketDBConnector
# from utils.models import (
#     BalanceSheetModel,
#     CashFlowModel,
#     DocumentModel,
#     IncomeStatementModel,
# )
#
# ALPHA_VANTAGE_KEY = environ["API_KEY"]
#

# class FinancialStatementsCollection(StockMarketDBConnector):
#     COLLECTION = "api_financialsdata"
#
#     def __init__(self):
#         super().__init__()
#         self.from_id = self.get_last_id()
#
#
# connection_kwargs = {
#     "user": "vYFyCTEJOyYWibhYuVxlnvezFuDHwGXI",
#     "password": "tD8Fpalp5GviRKn8zbBc0GdCIRWxynoqChkm4NaEG7g42lJgypqC1Iw8X7l6zAv5",
#     "host": "postgres",
#     "port": 5432,
#     "database": "stock_market_platform",
# }
# connection = psycopg2.connect(**connection_kwargs)
# cursor = connection.cursor()
#
#
# with DAG(
#     "alpha_vantage_dag",
#     start_date=days_ago(1),
#     schedule_interval=None,
#     max_active_runs=1,
# ) as alpha_vantage_dag:
#
#     def get_unavailable_symbols():
#         cursor.execute(
#             """SELECT * FROM financial_statements_statementsmetadata WHERE is_available = False"""
#         )
#
#         output = []
#         for row in cursor.fetchall():
#             output.append(
#                 DocumentModel(
#                     symbol=row[1], name=row[2], sector=row[7], industry=row[8]
#                 )
#             )
#         return output
#
#     def fetch_statements():
#         fields_processor = NormalizedFieldsProcessor("alpha_vantage", cursor)
#
#         income_statement_definition = IncomeStatementModel(
#             "INCOME_STATEMENT", fields_processor.mapped_source_fields
#         )
#         balance_sheet_definition = BalanceSheetModel(
#             "BALANCE_SHEET", fields_processor.mapped_source_fields
#         )
#         cash_flow_definition = CashFlowModel(
#             "CASH_FLOW", fields_processor.mapped_source_fields
#         )
#
#         unavailable_statements = get_unavailable_symbols()
#         mongo_cursor = FinancialStatementsCollection()
#
#         last_id = mongo_cursor.from_id
#
#         for obj in unavailable_statements:
#
#             for statement in [
#                 income_statement_definition,
#                 balance_sheet_definition,
#                 cash_flow_definition,
#             ]:
#                 url = f"https://www.alphavantage.co/query?
#                 function={statement.statement_type}&symbol={obj.symbol}&apikey={ALPHA_VANTAGE_KEY}"
#                 response = requests.get(url)
#                 print(response.json(), obj.symbol)
#                 data = response.json()["quarterlyReports"]
#                 statement.set_data(data)
#                 setattr(obj, statement.statement_type, statement.data)
#                 setattr(obj, "id", last_id)
#             mongo_cursor.collection.insert_one(obj.__dict__)
#             last_id += 1
#
#     alpha_vantage_task = PythonOperator(
#         task_id="alpha_vantage_task", python_callable=fetch_statements
#     )
