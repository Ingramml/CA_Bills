import os
import psycopg2
from Database_connection import get_postgres_connection

def run_sql_with_file(sql_path, data_file_path, conn):
    with open(sql_path, 'r') as f:
        sql = f.read()
    sql = sql.replace('{DATA_FILE_PATH}', data_file_path)
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()

def load_all_sql(sql_dir, data_dir, file_map):
    """
    Runs all SQL files in sql_dir, replacing {DATA_FILE_PATH} with the corresponding data file path.
    file_map: dict mapping sql filename (without .sql) to data filename (with extension)
    """
    conn = get_postgres_connection()
    if conn is None:
        print("Could not connect to the database.")
        return

    for sql_file_base, data_file_name in file_map.items():
        sql_path = os.path.join(sql_dir, f"{sql_file_base}.sql")
        data_file_path = os.path.join(data_dir, data_file_name)
        if not os.path.isfile(sql_path):
            print(f"SQL file not found: {sql_path}")
            continue
        if not os.path.isfile(data_file_path):
            print(f"Data file not found: {data_file_path}")
            continue
        print(f"Running {sql_path} with data {data_file_path}")
        try:
            run_sql_with_file(sql_path, data_file_path, conn)
            print(f"Loaded data for {sql_file_base}")
        except Exception as e:
            print(f"Error loading {sql_file_base}: {e}")
    conn.close()
    print("All done.")

if __name__ == "__main__":
    sql_dir = "/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation/SQL_files/Executes_Postgres"
    data_dir = "/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation/SQL_files"
    # Map SQL file base names to data file names
    file_map = {
        "bill_analysis_tbl": "BILL_ANALYSIS_TBL.dat",
        # Add more mappings as needed:
        # "another_table": "ANOTHER_TABLE.dat",
    }
    load_all_sql(sql_dir, data_dir, file_map)