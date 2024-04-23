import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import main
from load_data import DBType


def run_etl(stock_list, period, interval, drop_existing_table, db_type):
    main.run_pipeline(stock_list, period, interval, drop_existing_table, db_type)


# DAG arguments with default parameters
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 4, 22, 20, 0),  # Start at 8 PM
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "params": {
        "stock_list": ["AAPL"],
        "period": "1d",
        "interval": "1d",
        "drop_existing_table": True,
        "db_type": DBType.MYSQL.value,
    },
}

# Create the DAG
dag = DAG(
    "stock_etl_dag",
    default_args=default_args,
    start_date=datetime(2024, 4, 22),
    description="My DAG for executing functions once a day at 8 PM",
    schedule="@daily",
)

# Define a task to run the ETL function
task_run_etl = PythonOperator(
    task_id="run_load_stock_data_etl",
    python_callable=run_etl,
    op_args=[
        "{{ params.stock_list }}",
        "{{ params.period }}",
        "{{ params.interval }}",
        "{{ params.drop_existing_table}}",
        "{{ params.db_type}}",
    ],
    dag=dag,
)

# Set the task dependencies to define the execution order
task_run_etl
