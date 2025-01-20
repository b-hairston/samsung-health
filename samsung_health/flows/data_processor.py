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
    # validated_exercises_df = await convert_units(validated_exercises_df, 'exercises')

    float_columns = [col for col, dtype in validated_exercises_df.schema.items() if dtype == pl.Float64]
    datetime_columns = [col for col, dtype in validated_exercises_df.schema.items() if dtype == pl.Datetime]
    int_columns = [col for col, dtype in validated_exercises_df.schema.items() if dtype == pl.Int64]
    string_columns = [col for col, dtype in validated_exercises_df.schema.items() if dtype == pl.Utf8]

    validated_exercises_df = validated_exercises_df.with_columns([
        *[pl.col(col).fill_nan(0).alias(col) for col in float_columns],
        *[pl.col(col).fill_null(pl.datetime(1970, 1, 1)).alias(col) for col in datetime_columns],
        *[pl.col(col).fill_null(0).alias(col) for col in int_columns],  # Replace null with 0 for integers
        *[pl.col(col).fill_null("").alias(col) for col in string_columns],  # Replace null with an empty string for strings
])

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



# async def convert_units(df: pl.DataFrame, table_name: str) -> pl.DataFrame:
#     # Print initial DataFrame columns for debugging
#     print(f"Initial columns in {table_name}: {df.columns}")
#
#     if table_name == 'exercises':
#         if 'duration' in df.columns:
#             print("Converting 'duration' column to seconds...")
#             df = df.with_columns(
#                 (df['duration'] / 1000).cast(float).alias('duration')
#             )
#
#         if 'distance' in df.columns:
#             print("Converting 'distance' column to kilometers...")
#             df = df.with_columns(
#                 (df['distance'] / 1000).cast(float).alias('distance')
#             )
#
#         speed_columns = ['mean_speed', 'max_speed', 'min_speed']
#         for col in speed_columns:
#             if col in df.columns:
#                 print(f"Converting '{col}' column to km/h...")
#                 df = df.with_columns(
#                     (df[col] * 3.6).cast(float).alias(col)
#                 )
#
#     # Print the modified DataFrame columns for debugging
#     print(f"Modified columns in {table_name}: {df.columns}")
#     breakpoint()  # Inspect the data at this point
#     return df

