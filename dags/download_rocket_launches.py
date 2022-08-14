import os
import json
import requests

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.timezone import datetime


dag = DAG(
    dag_id="download_rocket_launches",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
)

download_launches = BashOperator(
    task_id="download_launches",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag
)


def _get_pictures():
    os.makedirs('/tmp/images', exist_ok=True)

    with open('/tmp/launches.json') as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches['results']]
        for image_url in image_urls:
            try:
                resp = requests.get(image_url)
                image_filename = image_url.split('/')[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, 'wb') as i:
                    i.write(resp.content)
                print(f"{image_url} is downloaded at {target_file}")
            except requests.exceptions.MissingSchema as MS:
                print(f"Invalid Image URL {image_url}")
                print(MS)
            except requests.exceptions.ConnectionError as CE:
                print(f"Could not connected to {image_url}")
                print(CE)


get_pictures = PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,
    dag=dag
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag
)

download_launches >> get_pictures >> notify
