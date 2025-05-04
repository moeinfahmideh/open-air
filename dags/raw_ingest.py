from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from open_air.ingest import airnow, openaq

default = dict(
    owner="data",
    retries=2,
    retry_delay=timedelta(minutes=5),
)

with DAG(
    dag_id="raw_ingest_hourly",
    start_date=datetime(2025, 5, 2),
    schedule_interval="@hourly",
    catchup=False,
    default_args=default,
    tags=["open-air"],
) as dag:
    t1 = PythonOperator(task_id="airnow_ingest", python_callable=airnow.ingest_sync)
    t2 = PythonOperator(task_id="openaq_ingest", python_callable=openaq.ingest_sync)
    t1 >> t2  # run AirNow first, then OpenAQ
