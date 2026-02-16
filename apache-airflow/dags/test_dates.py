from airflow.decorators import dag, task
from pendulum import datetime as pendulum_datetime


@dag(
    schedule="@Daily",  
    start_date=pendulum_datetime(2026, 2, 13, tz="Europe/Amsterdam"),
    catchup=True,
    tags=["test", "dates"],
)
def test_run_day_dates():
    @task
    def print_relevant_dates(**context):
        run_day = context["data_interval_start"].strftime("%Y-%m-%d")
        logical_date = context["logical_date"].strftime("%Y-%m-%d")
        data_interval_start = context["data_interval_start"].strftime("%Y-%m-%d %H:%M:%S")
        data_interval_end = context["data_interval_end"].strftime("%Y-%m-%d %H:%M:%S")
        ds = context["ds"]
        ts = context["ts"]

        print(f"Run Day (data_interval_start): {run_day}")
        print(f"Logical Date: {logical_date}")
        print(f"Data Interval Start: {data_interval_start}")
        print(f"Data Interval End: {data_interval_end}")
        print(f"ds: {ds}")
        print(f"ts: {ts}")

    # Just call the task; context is automatically provided by Airflow
    print_relevant_dates()

# Instantiate the DAG
dag = test_run_day_dates()