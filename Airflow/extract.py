import pandas as pd
import psycopg2
import pandas as pd
from google.cloud import bigquery

def get_tables():
    conn = psycopg2.connect(
            database = "db_adwoltp",
            user = "postgres",
            host= 'localhost',
            password = "password",
            port = 5432)
    cursor = conn.cursor()

    cursor.execute(f"""SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'""")

    tbls = [x[0] for x in cursor.fetchall()]

def extract_load(tbls, conn):

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")


    for tbl in tbls:
        table_id = f"adventureworks-431609.stg.{tbl}"
        sql = f"SELECT * FROM {tbl} WHERE updated_at >= '2024-08-12'"
        df = pd.read_sql(sql, conn)


        job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config)
    job.result()