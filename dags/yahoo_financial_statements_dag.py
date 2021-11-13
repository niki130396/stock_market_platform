from os import environ

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

airflow_home = environ["AIRFLOW_HOME"]

with DAG(
    "yahoo_financial_statements_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    max_active_runs=1,
) as yahoo_financial_statements_dag:

    crawl_yahoo_finance = BashOperator(
        task_id="crawl",
        bash_command="cd ${AIRFLOW_HOME}/scrapy_tasks &&"
        " scrapy crawl yahoo_finance_statements_spider",
    )
