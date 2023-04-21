from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

k = KubernetesPodOperator(
    name="hello-dry-run",
    image="debian",
    cmds=["bash", "-cx"],
    arguments=["echo", "10"],
    labels={"foo": "bar"},
    task_id="dry_run_demo",
    do_xcom_push=True,
)

# k.dry_run()


import datetime
import pendulum

from airflow import DAG

with DAG(
    dag_id="example_pod_task",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval=None,
    dagrun_timeout=datetime.timedelta(minutes=10),
    tags=["dev", "sync", "manual"],
) as dag:
    k = KubernetesPodOperator(
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        do_xcom_push=True,
    )

    k

if __name__ == "__main__":
    KubernetesPodOperator(
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["'echo 10'"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        do_xcom_push=True,
    ).dry_run()
