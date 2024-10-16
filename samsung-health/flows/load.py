import asyncio

import pandas as pd 

from prefect import task
from models import Exercise
#load csv files, in future, will have util function to download from S3

# @task()
async def load_data():
    exercise_df = pd.read_csv(
        '/home/imani/Documents/Data/com.samsung.shealth.exercise.20240918124865.csv',
         dtype=str,
         skiprows=1 )





async def process_exercises(exercise_df: pd.DataFrame) -> exersises: List:
    exercises = []
    
    # Iterate over the DataFrame rows and validate with Pydantic
    for _, row in exercise_df.iterrows():
        try:
            # Create an Exercise instance using the row data
            exercise = Exercise(
                start_time=row['startTime'],
                end_time=row['endTime'],
                total_calorie=row.get('totalCalorie'),
                distance=row.get('distance'),
                duration=row.get('duration'),
                exercise_type=row.get('exerciseType')
            )
            
            # Append to the list of valid exercises
            exercises.append(exercise)
        except Exception as e:
            print(f"Error parsing row: {e}")
        
    breakpoint()
