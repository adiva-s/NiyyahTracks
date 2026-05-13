from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging


# ============================================================
# NiyyahTrack v2 — Cloud Pipeline DAG
# ============================================================
# Pipeline: BigQuery seed → dbt transformations → dbt tests
#
# Task 1 | seed_bigquery
#   Generates synthetic Islamic charitable giving data using
#   Faker and loads raw tables into BigQuery (niyyahtrack dataset):
#   donor, charity, project, testimonials, donation
#
# Task 2 | dbt_run
#   Runs dbt models against BigQuery — staging models clean
#   and standardize raw tables, mart models produce analytics-
#   ready aggregations (e.g. total raised per charity)
#
# Task 3 | dbt_test
#   Runs dbt tests to validate data integrity — checks for
#   nulls, uniqueness, and referential integrity across models
# ============================================================


def on_failure_callback(context):
    """Logs task failure details for debugging."""
    logging.error(
        f"Task FAILED | DAG: {context['task_instance'].dag_id} | "
        f"Task: {context['task_instance'].task_id} | "
        f"Date: {context['execution_date']} | "
        f"Log URL: {context['task_instance'].log_url}"
    )


default_args = {
    'owner': 'adiva',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_callback,
}

with DAG(
    dag_id="niyyahtrack_dbt",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    description="NiyyahTrack v2 — end-to-end cloud pipeline: seeds BigQuery, runs dbt models and tests daily",
    tags=["dbt", "niyyahtrack", "bigquery", "gcp"],
) as dag:

    # Task 1: Generate and load raw data into BigQuery
    seed_bigquery = BashOperator(
        task_id="seed_bigquery",
        bash_command="python /opt/airflow/niyyah_tracks/seed.py",
    )

    # Task 2: Run dbt transformations (staging + marts)
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/niyyah_tracks/niyyah_dbt && dbt run --profiles-dir /home/airflow/.dbt",
    )

    # Task 3: Validate data quality with dbt tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/niyyah_tracks/niyyah_dbt && dbt test --profiles-dir /home/airflow/.dbt",
    )

    # Pipeline execution order
    seed_bigquery >> dbt_run >> dbt_test