from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

#  Try this comment
with DAG(
    "test_dag", start_date=days_ago(1), schedule_interval=None, max_active_runs=1
) as test_dag:

    def run_task():
        return [i for i in range(100)]

    fetch_statements_task = PythonOperator(
        task_id="fetch_statements", python_callable=run_task
    )

    trigger_dag = TriggerDagRunOperator(
        task_id="trigger_test_dag",
        trigger_dag_id="test_dag",
        allowed_states=["success", "failed"],
    )

    fetch_statements_task >> trigger_dag
