from airflow import DAG
from airflow.timetables.trigger import CronTriggerTimetable
from airflow.sdk import task  # Updated import
import pendulum  # Added import

with DAG(
    dag_id="test_run_day_dates",
    schedule=CronTriggerTimetable("0 0 * * *", timezone="Europe/Amsterdam"),
    start_date=pendulum.datetime(2026, 2, 13, tz="Europe/Amsterdam"),
    catchup=True,
    tags=["test", "dates"],
) as dag:

    @task
    def print_relevant_dates(**context):
        tz = pendulum.timezone("Europe/Amsterdam")

        # Convert all timestamps to the Amsterdam timezone
        data_interval_start = context["data_interval_start"].in_timezone(tz)
        data_interval_end = context["data_interval_end"].in_timezone(tz)
        logical_date = context["logical_date"].in_timezone(tz)
        ts = pendulum.parse(context["ts"]).in_timezone(tz)

        # Format timestamps for printing
        previous_day = data_interval_start.strftime("%Y-%m-%d")
        logical_date_str = logical_date.strftime("%Y-%m-%d")
        data_interval_start_str = data_interval_start.strftime("%Y-%m-%d %H:%M:%S")
        data_interval_end_str = data_interval_end.strftime("%Y-%m-%d %H:%M:%S")
        ds = context["ds"]
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")

        # Print the results
        print(f"Previous Day (data_interval_start): {previous_day}")
        print(f"Logical Date (data_interval_end): {logical_date_str}")
        print(f"Data Interval Start (Amsterdam): {data_interval_start_str}")
        print(f"Data Interval End (Amsterdam): {data_interval_end_str}")
        print(f"ds: {ds}")
        print(f"ts: {ts_str}")

    print_relevant_dates()
