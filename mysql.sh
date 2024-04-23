#!/usr/bin/env bash
CONTAINER_NAME="final_project_airflow_webserver_1"
USER_NAME="airflow_user"
PASSWORD="airflow_pass"
docker exec ${CONTAINER_NAME} mysql -u ${USER_NAME} -p${PASSWORD} -e 'SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";SET time_zone = "+00:00";'