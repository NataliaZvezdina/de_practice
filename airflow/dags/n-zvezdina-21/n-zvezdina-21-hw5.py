"""
The DAG works with API(https://rickandmortyapi.com/documentation/#location),
find the top three locations on "Rick and Morty" with the most residents,
load resulting data to GreenPlum.
"""

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator

from n_zvezdina_21_plugins.n_zvezdina_21_ram_top_locations_operator import NZvezdina21RamTopLocationsOperator

DEFAULT_ARGS = {
    'start_date': days_ago(1),
    'owner': 'n-zvezdina-21'
}

with DAG('n-zvezdina-21-hw5',
         schedule_interval='@once',
         max_active_runs=1,
         default_args=DEFAULT_ARGS,
         tags=['n-zvezdina-21']
         ) as dag:

    prepare_gp_table = PostgresOperator(
        task_id="prepare_gp_table",
        postgres_conn_id="conn_greenplum_write",
        sql="""
            CREATE TABLE IF NOT EXISTS n_zvezdina_21_ram_location(
                id INT,
                name VARCHAR,
                type VARCHAR,
                dimension VARCHAR,
                resident_cnt INT
            );
            TRUNCATE TABLE n_zvezdina_21_ram_location;
            """,
    )

    extract_from_api = NZvezdina21RamTopLocationsOperator(task_id="extract_from_api")

    load_to_gp = PostgresOperator(
        task_id="load_to_gp",
        postgres_conn_id="conn_greenplum_write",
        sql="INSERT INTO n_zvezdina_21_ram_location VALUES {{ ti.xcom_pull(task_ids='extract_from_api') }}"
    )

    prepare_gp_table >> extract_from_api >> load_to_gp
