# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# ENV AIRFLOW_HOME=/usr/src/app
# ENV AIRFLOW__CORE__DAGS_FOLDER=/usr/src/app/airflow/dags

ENV PYTHONPATH=/usr/src/app
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
