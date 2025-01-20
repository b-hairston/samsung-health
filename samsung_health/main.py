import asyncio  

from prefect import Flow, task
from flows.data_loader import load_data
from flows.data_processor import process_exercises
from flows.postgres import write_db, get_connection
from flows.models import Exercise
import polars as pl 

async  def main():
    print("hello")
    exercise_df = await load_data()
    validated_ex_df = await process_exercises(exercise_df)
    conn = get_connection()
    table_config  = {
        "exercises":{
            "primary_key": "data_uuid",
            "model": Exercise
        }
    }
  
    await write_db(conn,validated_ex_df, table_config, 'exercises' )
   

if __name__ == "__main__":
    asyncio.run(main())
