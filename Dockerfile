# Use the official Python image as the base image
FROM python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

ENV AIRFLOW_HOME=/usr/src/app
# Do not load the example dags
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false 


ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=mysql://airflow_user:airflow_pass@mysql:3306/airflow_db
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor
ENV PYTHONPATH=/usr/src/app
ENV ENV=PROD
# create a directory for the app on the container(linux based system)  
RUN mkdir /usr/src/app
# set the working directory to the directory created above
WORKDIR /usr/src/app
# copy the requirements file to the working directory
COPY requirements.txt ./

# Set the DAGs folder path

# COPY ./airflow/dags/. ./dags 

# install the dependencies
RUN pip install -r requirements.txt


# copy the content of the local src directory to the working directory
COPY . .
RUN chmod +x entrypoint.sh