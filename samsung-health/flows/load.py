import pandas as pd 
from prefect import task
#load csv files, in future, will have util function to download from S3

# @task()
def load_data():
    exercise_df = pd.read_csv(
        '/home/imani/Documents/Data/com.samsung.shealth.exercise.20240918124865.csv',
         dtype=str,
         skiprows=1 )
    breakpoint()
