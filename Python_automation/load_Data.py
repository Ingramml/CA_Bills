import os
import psycopg2
from Database_connection import get_postgres_connection

def load_sql_files(sql_dir, schema="public"):
    """
    This script loads data into PostgreSQL tables using SQL files with a {DATA_FILE_PATH} placeholder.
    
    For each table listed in tables_lc.lst (located in sql_dir), it:
    - Finds the corresponding .sql (PostgreSQL COPY statement) and .dat (data) files.
    - Replaces the {DATA_FILE_PATH} placeholder in the SQL with the actual .dat file path.
    - Executes the SQL to load data into the database.
    - Logs the result for each table in a logs/ directory.
    
    Requirements:
    - SQL files must use the {DATA_FILE_PATH} placeholder for the data file path.
    - Data files and SQL files must be named after the table (e.g., mytable.sql, MYTABLE.dat).
    - Database connection is handled by get_postgres_connection() from Database_connection.py.
    """
    
    table_list_file = os.path.join(sql_dir, "tables_lc.lst")
    conn = get_postgres_connection()
    if conn is None:
        print("Could not connect to the database.")
        return

    logs_dir = os.path.join(sql_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    with open(os.path.join(sql_dir, table_list_file)) as f:
        for line in f:
            table = line.strip()
            if not table:
                continue
            dat_file = os.path.join(sql_dir, f"{table}.dat")
            sql_file = os.path.join(sql_dir, f"{table}.sql")
            log_file = os.path.join(logs_dir, f"{table}.log")
            if os.path.isfile(dat_file):
                print(f"Processing table: {table}")
                try:
                    with open(sql_file, "r") as sql_input, open(log_file, "w") as log_output:
                        sql_script = sql_input.read()
                        with conn.cursor() as cur:
                            cur.execute(sql_script)
                            conn.commit()
                            log_output.write(f"Executed {sql_file} successfully.\n")
                except Exception as e:
                    print(f"Error processing {table}: {e}")
                    with open(log_file, "a") as log_output:
                        log_output.write(f"Error: {e}\n")
            else:
                print(f"Skipping {table}: {dat_file} not found")
    conn.close()
    print("Done.")

if __name__ == "__main__":
    # You can pass sql_dir as an argument or set it here
    sql_dir = "/Users/michaelingram/Documents/GitHub/CA_Bills/Sqlfiles"
    load_sql_files(sql_dir)