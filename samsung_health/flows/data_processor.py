import asyncio
import polars as pl

from datetime import datetime, timezone 
from pydantic import ValidationError
from typing import List
from prefect import task
from flows.models import Exercise

async def process_exercises(exercise_df: pl.DataFrame) -> List[Exercise]:
    exercises = []

    # Iterate over the Polars DataFrame rows
    for row in exercise_df.to_dicts():
        try:
            exercise = Exercise(**row)  # Use Pydantic model to validate row data
            exercises.append(exercise)
        except ValidationError as e:
            print(f"Validation error for row: {row}\nError: {e}")
    validated_exercises_df = await dicts_to_df(exercises)
    # convert ms to seconds
    validated_exercises_df = validated_exercises_df.with_columns(
        (validated_exercises_df['duration'] / 1000).cast(int).alias('duration'))

    #drop empty columns
    validated_exercises_df= validated_exercises_df.drop(['mean_power',
            'max_power',
            'mean_caloric_burn_rate',
            'max_caloric_burn_rate',
            'mean_rpm',
            'max_rpm',
            'custom',
            'title'])
    validated_exercises_df= validated_exercises_df.select([
        pl.col(col).fill_nan(pl.lit(0) if dtype in [pl.Int64, pl.Float64] else pl.lit('Unknown'))
        for col, dtype in zip(validated_exercises_df.columns, validated_exercises_df.dtypes)])
    # write df to file
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"data/{timestamp}_exercises.parquet"
    validated_exercises_df.write_parquet(filename)
    validated_exercises_df.write_csv("yee.csv")


    return validated_exercises_df

async def dicts_to_df(exercises: List[Exercise]) -> pl.DataFrame:
    try:
        # Convert list of Pydantic objects to a list of dictionaries
        dicts = [exercise.dict() for exercise in exercises]
        
        # Convert to Polars DataFrame
        df = pl.from_dicts(dicts)
        return df
    except Exception as e:
        print(f"Error while converting to DataFrame: {e}")
        return pl.DataFrame()  # Return an empty DataFrame in case of error
 
