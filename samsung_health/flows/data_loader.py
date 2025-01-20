import asyncio
import polars as pl
import glob
import os
from typing import List
from prefect import task
from flows.models import Exercise
#load csv files, in future, will have util function to download from S3

# @task()
async def find_files_with_pattern(directory, pattern):
    """
    Searches the given directory for files matching the specified pattern.

    Args:
        directory (str): The directory to search in.
        pattern (str): The pattern to match files.

    Returns:
        list: A list of file paths that match the pattern.

    """
    all_files = glob.glob(os.path.join(directory, f"*{pattern}*"))    
    csv_files = [file for file in all_files if file.endswith('.csv')]
    return csv_files    
async def load_data():
    """
    Loads data from all files matching the pattern "com.samsung.shealth.exercise".

    Returns:
        pl.DataFrame: The combined Polars DataFrame from all matching files.
    """
    directory = "/home/imani/Documents/Data"
    pattern = "com.samsung.shealth.exercise.2"

    # Find files matching the pattern
    matching_files = await find_files_with_pattern(directory, pattern)

    if not matching_files:
        raise FileNotFoundError(f"No files matching the pattern '{pattern}' were found in '{directory}'.")

    print(f"Found {len(matching_files)} files matching the pattern.")

    # Load all matching files and combine them
    all_data = []
    common_columns = None
    
    for file_to_load in matching_files:
        print(f"Loading file: {file_to_load}")
        exercise_df = pl.read_csv(
            file_to_load,
            skip_rows=1,
            truncate_ragged_lines=True,
            ignore_errors=True
        )
        file_columns = exercise_df.columns
        
        # If it's the first file, set its columns as the common columns
        if common_columns is None:
            common_columns = file_columns
        else:
            # Ensure both files have the same columns, add missing ones with None/NaN values
            missing_columns = set(common_columns) - set(file_columns)
            extra_columns = set(file_columns) - set(common_columns)

            # Add missing columns (set to None) to the current file DataFrame
            for col in missing_columns:
                exercise_df = exercise_df.with_columns(pl.lit(None).alias(col))

            # Remove extra columns
            exercise_df = exercise_df.select(common_columns)
        all_data.append(exercise_df)
    
    # Combine the DataFrames into one

    combined_df = pl.concat(all_data)
    return combined_df

 
