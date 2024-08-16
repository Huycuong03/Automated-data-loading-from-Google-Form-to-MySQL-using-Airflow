from datetime import datetime, timedelta
from scripts.responses_to_json import responses_to_json
from scripts.json_to_sql import json_to_sql
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'hc03',
    'retries': '3',
    'retry_delay':timedelta(minutes=1)
}

with DAG(
    dag_id='forms_to_sql_v11',
    default_args=default_args,
    start_date=datetime(2024, 8, 14, 7),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='task1',
        python_callable=responses_to_json
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=json_to_sql
    )

    task1 >> task2