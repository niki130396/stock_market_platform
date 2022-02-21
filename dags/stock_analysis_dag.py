from os import environ

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

airflow_home = environ["AIRFLOW_HOME"]

with DAG(
    "stock_analysis_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    max_active_runs=1,
) as stock_analysis_dag:

    crawl_stock_analysis_dot_com = BashOperator(
        task_id="crawl",
        bash_command="cd ${AIRFLOW_HOME}/scrapy_tasks &&"
        " scrapy crawl stock_analysis_spider",
    )

    sleep_for_ten_minutes = BashOperator(task_id="sleep", bash_command="sleep 600")

    retrigger_dag = TriggerDagRunOperator(
        task_id="retrigger_dag",
        trigger_dag_id="stock_analysis_dag",
        allowed_states=["success", "failed"],
    )

    crawl_stock_analysis_dot_com >> sleep_for_ten_minutes >> retrigger_dag
