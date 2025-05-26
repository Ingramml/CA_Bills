import os
import pandas as pd
from sqlalchemy import create_engine
from Database_connection2 import get_postgres_connection_sqlalchemy  # This should return a SQLAlchemy connection string

def upload_to_postgres(input_data, table_name, schema="public"):
    """
    Uploads a CSV file or pandas DataFrame to a PostgreSQL table using SQLAlchemy.

    Args:
        input_data: Path to CSV file or a pandas DataFrame.
        table_name: Name of the target table in PostgreSQL.
        schema: Schema name (default: 'public').
    """
    # Load data into DataFrame
    if isinstance(input_data, pd.DataFrame):
        df = input_data
    elif isinstance(input_data, str) and os.path.isfile(input_data) and input_data.lower().endswith('.csv'):
        df = pd.read_csv(input_data)
    else:
        raise ValueError("input_data must be a pandas DataFrame or a path to a CSV file.")

    # Get SQLAlchemy connection string from your connection utility
    conn_str = get_postgres_connection_sqlalchemy()
    engine = create_engine(conn_str)

    try:
        df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False, method='multi')
        print(f"Data uploaded to {schema}.{table_name} successfully.")
    except Exception as e:
        print(f"Error uploading data to {schema}.{table_name}: {e}")
    finally:
        engine.dispose()

# Example usage:
if __name__ == "__main__":
    # As DataFrame
    # df = pd.DataFrame({'a': [1,2], 'b': [3,4]})
    # upload_to_postgres(df, "my_table", schema="ca_public")
    input_data = '/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/2025-05-25/Bill_Version.csv'
    table_name = "Bill_Version"
    # As CSV file
    upload_to_postgres(input_data, table_name, schema="capublic")