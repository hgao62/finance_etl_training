#!/usr/bin/env bash
airflow db init
airflow users create --username admin --password admin --firstname kobe --lastname Gao --role Admin --email hgao62@uwo.ca
airflow webserver -p 8080
ECHO "Airflow webserver is running"
ECHO "About to run Airflow scheduler"
airflow scheduler
ECHO "irflow scheduler is running"