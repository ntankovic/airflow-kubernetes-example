import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

with DAG(
    dag_id="prod_to_dev_sync",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval=None,
    dagrun_timeout=datetime.timedelta(minutes=10),
    tags=["dev", "sync", "manual"],
    params={"sources": ["sales", "trips", "actions"]},
) as dag:
    merge = EmptyOperator(
        task_id="finish",
    )

    def branch_tasks(**context):
        print("Local parameters", context["dag_run"].conf.get("sources"))
        print("Default parameters", context["dag"].params.get("sources"))
        print("Default parameters #2", dag.params.get("sources"))
        return context["dag_run"].conf.get("sources")

    branching = BranchPythonOperator(
        task_id="sync_tasks", provide_context=True, python_callable=branch_tasks
    )

    for source in dag.params["sources"]:
        task = BashOperator(
            task_id=source,
            bash_command=f'echo "{source}" && sleep 1',
        )
        branching >> task >> merge

    # branching >> [sales, trips, actions] >> merge

if __name__ == "__main__":
    dag.test(run_conf={"sources": ["actions"]})
