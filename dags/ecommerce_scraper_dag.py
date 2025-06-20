from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags.scripts.advice_scraper import scrape_advice
from dags.scripts.jaymartstore_scraper import scrape_jaymartstore
from dags.scripts.price_comparison import compare_prices
from dags.scripts.google_drive_upload import upload_to_gdrive
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecommerce_price_comparison',
    default_args=default_args,
    description='Daily E-commerce Price Comparison',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def scrape_and_compare(**kwargs):
    advice_df = scrape_advice()
    jaymartstore_df = scrape_jaymartstore()
    comparison_df = compare_prices(jaymartstore_df, advice_df)

    today = datetime.now().strftime('%Y-%m-%d')
    file_path = f'/tmp/ecommerce_price_comparison_{today}.xlsx'

    os.makedirs('/tmp', exist_ok=True)

    with pd.ExcelWriter(file_path) as writer:
        comparison_df.to_excel(writer, sheet_name='Price Comparison', index=False)

    return file_path

def upload_to_drive(**kwargs):
    ti = kwargs['ti']
    file_path = ti.xcom_pull(task_ids='scrape_and_compare')

    folder_id = '12vFoPKik3p2khDKwBxgSRCcjIsrA-Zkp'
    upload_to_gdrive(file_path, folder_id)

scrape_task = PythonOperator(
    task_id='scrape_and_compare',
    python_callable=scrape_and_compare,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_drive',
    python_callable=upload_to_drive,
    dag=dag,
)

scrape_task >> upload_task
