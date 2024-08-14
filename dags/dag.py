from datetime import datetime, timedelta
from formtojson import formtojson
from jsontocsv import jsontocsv
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'hc03',
    'retries': '3',
    'retry_delay':timedelta(minutes=1)
}

with DAG(
    dag_id='forms_to_sql_v1',
    default_args=default_args,
    start_date=datetime(2024, 8, 14, 7),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='task1',
        python_callable=formtojson
    )

    # task2 = PythonOperator(
    #     task_id='task2',
    #     python_callable=jsontocsv
    # )
    task1