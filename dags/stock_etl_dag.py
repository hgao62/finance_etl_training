import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from main import main


def run_etl(stock_list, period, interval):
    main(stock_list, period, interval)


# DAG arguments with default parameters
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 4, 22, 20, 0),  # Start at 8 PM
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "params": {
        "stock_list": ["AAPL"],
        "period": "1d",
        "interval": "1d",
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
    op_args=["{{ params.stock_list }}", "{{ params.period }}", "{{ params.interval }}"],
    dag=dag,
)

# Set the task dependencies to define the execution order
task_run_etl
