import psycopg2

from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime 
from typing import Optional, Union


import numpy
import polars as pl
import os


load_dotenv()

# Get the password from environment variables

postgres_password = os.getenv("POSTGRES_PASSWORD")

# Function to establish a connection
def get_connection():
    
    return psycopg2.connect(
        dbname="postgres",           # Default database name
        user="postgres",             # Default user
        password=postgres_password,  # Password from .env file
        host="localhost",            # Host is localhost
        port="5432"                  # Default PostgreSQL port
    )

# Function to execute a query using the passed connection
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()  # Fetch all results from the query
    cursor.close()
    return result

def generate_table_sql(model: BaseModel, df: pl.DataFrame, table_name: str, primary_key: str = 'id') -> str:
    """
    Generate a SQL CREATE TABLE statement from a Pydantic model, considering only columns present in the DataFrame.
    
    :param model: Pydantic model class
    :param df: Polars DataFrame containing the data
    :param table_name: The name of the table to create
    :param primary_key: The column to be used as the primary key (default is 'id')
    :return: SQL CREATE TABLE statement
    """
  

    columns = []
    # Iterate over the fields in the Pydantic model
    for field_name, field_type in model.__annotations__.items():
        # Only include fields present in the DataFrame
        if field_name in df.columns:
            column_definition = f"{field_name} {get_sql_type(field_type)}"
        
            # Handle Optional fields (nullable)
            if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                # Extract the arguments for Union
                args = field_type.__args__
                if type(None) in args:
                    # If None is in the Union, it means the field is Optional, so it's nullable
                    column_definition += " NULL"
                else:
                    # Otherwise, it's NOT NULL by default
                    column_definition += " NOT NULL"
            else:
                # Default behavior for non-Optional fields
                column_definition += " NOT NULL"
        
            # Handle primary key case: primary key should always be NOT NULL
            if field_name == primary_key:
                column_definition += " PRIMARY KEY"
        
            columns.append(column_definition)
    
    # Add primary key definition if it's not already specified in the model
    if primary_key not in model.__annotations__:
        columns.append(f"{primary_key} SERIAL PRIMARY KEY")
    
    # Join all column definitions into the SQL statement
    columns_str = ",\n    ".join(columns)
     
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns_str}
    );
    """

  
    return create_table_query


def get_sql_type(field_type):
    """
    Maps Pydantic field types to PostgreSQL column types.
    
    :param field_type: Python type
    :return: Corresponding PostgreSQL type
    """
    # Check for Optional[X] fields
    if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
        # Extract the arguments for Union
        args = field_type.__args__
        if type(None) in args:
            # Handle Optional case by checking the actual type (ignoring None)
            field_type = next(arg for arg in args if arg is not type(None))

    # Map to PostgreSQL data types
    if field_type == int:
        return "BIGINT"
    elif field_type == float:
        return "DOUBLE PRECISION"
    elif field_type == str:
        return "TEXT"
    elif field_type == bool:
        return "BOOLEAN"
    elif field_type == datetime:
        return "TIMESTAMP"
    else:
        raise ValueError(f"Unsupported field type: {field_type}")


def create_table(model: BaseModel, df: pl.DataFrame, table_name: str, primary_key: str):
    # Generate the CREATE TABLE SQL query
    create_table_query = generate_table_sql(model, df, table_name, primary_key)
    
    # Connect to PostgreSQL and execute the query
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)  # Execute the create table query
            connection.commit()  # Commit changes to the database
            print(f"Table '{table_name}' created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        connection.close()

async def write_db(connection, df: pl.DataFrame, table_config: dict, table_key: str):
    print(f"Connection type: {type(connection)}")
    """
    Asynchronously write data from a Polars DataFrame to the specified PostgreSQL table.
    
    :param connection: psycopg2 connection object
    :param df: Polars DataFrame containing the data
    :param table_name: Name of the table where data will be written
    :param primary_key: Primary key column (default is 'id')
    """
    config = table_config.get(table_key)
    if not config:
        raise ValueError(f"Configuration for {table_key} not found.")
    
    primary_key = config.get("primary_key", "id")
    model = config.get("model")

    # Ensure the table exists before inserting data
    create_table(model, df, table_key, primary_key)

    # Convert Polars DataFrame to a list of tuples (suitable for insertion)
    records = df.to_numpy().tolist()
   
    # Define column names based on the DataFrame
    columns = df.columns

    merge_query = f"""
    MERGE INTO {table_key} AS target
    USING (SELECT {', '.join(['%s'] * len(columns))}) AS source ({', '.join(columns)})
    ON target.{primary_key} = source.{primary_key}
    WHEN MATCHED THEN
        UPDATE SET {', '.join([f"{col} = source.{col}" for col in columns if col != primary_key])}
    WHEN NOT MATCHED THEN
        INSERT ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))});
    """

   
    try:
        with connection.cursor() as cursor:
            for record in records:
                cursor.execute(merge_query, record + record)  # Duplicate record for UPDATE and INSERT
            connection.commit()
            print(f"Inserted {len(records)} rows into the {table_key} table.")
    except Exception as e:
        print(f"Error inserting data: {e}")

