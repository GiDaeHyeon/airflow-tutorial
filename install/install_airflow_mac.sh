#!/bin/sh

export AIRFLOW_HOME=~/airflow

brew install mysql
brew install redis

AIRFLOW_VERSION=2.2.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install -U pip
pip install pymysql
pip install "apache-airflow[mysql,redis]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

brew services start mysql
brew services start redis

# 만약에 외부 데이터베이스와 연결하게 된다면, ip, id, pw를 바꿔줘야겠죠??
# 아마 현업에서는 당연히 변경해서 실행시켜야 할 것!
mysql -h 127.0.0.1 -u root < create_database.sql
