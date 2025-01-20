import asyncio
import polars as pl

from typing import List
from prefect import task
from flows.models import Exercise
#load csv files, in future, will have util function to download from S3

# @task()
async def load_data():
    exercise_df = pl.read_csv(
    '/home/imani/Documents/Data/com.samsung.shealth.exercise.20240918124865.csv',
    skip_rows=1,
    truncate_ragged_lines=True,
    ignore_errors=True)

    return exercise_df  
 
