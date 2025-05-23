import os
import psycopg2
from Database_connection import get_postgres_connection

def load_table_from_sql(sql_file_path, data_file_path):
    # Read SQL file and replace placeholder
    with open(sql_file_path, 'r') as f:
        sql = f.read().replace('{DATA_FILE_PATH}', data_file_path)
    conn = get_postgres_connection()
    if conn is None:
        print("Could not connect to the database.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
            print(f"Loaded data from {data_file_path} into table.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    sql_file = "/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation/SQL_files/Executes_Postgres/bill_analysis_tbl.sql"
    data_file = "/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation/SQL_files/BILL_ANALYSIS_TBL.dat"
    load_table_from_sql(sql_file, data_file)