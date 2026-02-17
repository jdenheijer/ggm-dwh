from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.hooks.base import BaseHook
from datetime import datetime
import requests
import re
from zipfile import ZipFile
import os
import pandas as pd
from airflow.timetables.trigger import CronTriggerTimetable

DATA_DIRECTORY = '/tmp'

with DAG(
    dag_id="get_rxm_data",
    start_date=datetime(2026, 2, 17),
    catchup=False,
    tags=["rxm"],
    schedule=CronTriggerTimetable("0 1 * * *", timezone="utc"),
) as dag:

    @task()
    def prepare_download():
        #determine run date, check previous run, create folder

    @task()
    def download_zip():
        # Get Variable
        api_url = Variable.get("rxm_api_biexport_url")
        # Get Connection
        conn = BaseHook.get_connection("rxm_api")
        username = conn.login
        password = conn.password
        response = requests.get(api_url, auth=(username, password))
        if response.status_code == 200:
            # Find filename in header, fallback if not found
            content_disposition = response.headers.get('Content-Disposition')
            filename = (
                re.search(r'filename="?([^";]+)"?', content_disposition).group(1)
                if content_disposition and re.search(r'filename="?([^";]+)"?', content_disposition)
                else 'downloaded_file.zip'
            )
            file_path = os.path.join(DATA_DIRECTORY, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path  # Pass file path to next task
        else:
            raise Exception(
                f"Failed to download file. Status code: {response.status_code}\nResponse: {response.text}"
            )

    @task()
    def unzip_file(zip_file_path: str, **context):
        # Retrieve logical date from DAG context and determine the data_date
        logical_date = context['logical_date']
        data_date = logical_date - timedelta(days=1)
        # Format logical date as YYYY-MM-DD
        data_date_str = data_date.strftime('%Y-%m-%d')

        # Create extraction path using data date
        extract_path = os.path.join('/tmp/rxm', data_date_str)
        os.makedirs(extract_path, exist_ok=True)

        with ZipFile(zip_file_path, 'r') as zObject:
            zObject.extractall(extract_path)
            print(f"Files extracted to {extract_path}")
        return extract_path  # Pass extract path to next task

    @task()
    def load_bi_export_inhoud(extract_path: str):
        # Path to the CSV file in the extracted data
        csv_path = os.path.join(extract_path, "bi-export-inhoud.csv")
        # Load CSV into pandas DataFrame
        df = pd.read_csv(csv_path)
        print(f"Loaded DataFrame with {df.shape[0]} rows and {df.shape[1]} columns.")
        print(df.head())
        return df.to_json()

    zip_file = download_zip()
    extracted_dir = unzip_file(zip_file, dag=dag)
    load_bi_export_inhoud(extracted_dir)