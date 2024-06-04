from load_csv_utils import load_csv_sql  
from zip_directory_util import zip_directory  
from upload_s3_util import upload_directory_to_s3 
from comodity import run_fetch_comodity  
from economy import fetch_gdp_data 

from airflow import DAG
from airflow.operators.bash_operator import BashOperator 
from airflow.operators.python_operator import PythonOperator 
from airflow.operators.postgres_operator import PostgresOperator  
from airflow.utils.dates import days_ago
import os
from datetime import timedelta

output = "/opt/airflow/output"

default_args = {
    'owner': 'John',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['jtamakloe6902@gmal.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Econdb',
    default_args=default_args,
    description='Fetch Comodity Daily',
    schedule_interval='@daily',
)

# fetch comodities
fetch_comodity = PythonOperator(
    task_id="fetch_comodity",
    python_callable=run_fetch_comodity,
    dag = dag  
)

economy_data = PythonOperator(
    task_id="economy_data",
    python_callable=fetch_gdp_data,
    dag = dag
) 
 
# load csv files to PostgreSQL DB
load_to_db = PythonOperator(
    task_id="load_to_db",
    python_callable=load_csv_sql,
    op_kwargs={
        "file_dir": output,
        "output_directory":output,
        "username": os.getenv("username"),
        "password": os.getenv("password"),
        "database": os.getenv("database"),
        "host": os.getenv("host"),
        "port": os.getenv("port")
        },
    dag = dag
)

# Zip all files in csv folder
zip_files = PythonOperator(
    task_id="zip_files",
    python_callable=zip_directory,
    op_kwargs = {"directory_path":output,
                 "zip_path":os.path.join(output,"data.zip")
                 },
    dag = dag )


# load data to s3 
load_to_s3 = PythonOperator(
    task_id="load_to_s3",
    python_callable=upload_directory_to_s3,
    op_kwargs = {"directory_path": output},
    dag = dag
)   


fetch_comodity >> load_to_db
economy_data >> load_to_db
load_to_db >> zip_files >> load_to_s3 
