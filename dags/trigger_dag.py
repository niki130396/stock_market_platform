from airflow.models import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

with DAG(
    "trigger_dag",
    start_date=days_ago(1),
    schedule_interval="*/10 * * * *",
    max_active_runs=1,
) as trigger_dag:

    trigger_test_dag = TriggerDagRunOperator(
        task_id="trigger_test_dag",
        trigger_dag_id="stock_analysis_dag",
        allowed_states=["success", "failed"],
        wait_for_completion=True,
    )
