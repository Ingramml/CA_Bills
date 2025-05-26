import os
import psycopg2
from Database_connection import get_postgres_connection
from dotenv import load_dotenv

load_dotenv()

def create_database_if_not_exists():
    """Create the target database if it does not exist, using env vars."""
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)

    # Connect to the default 'postgres' database to create a new one if needed
    conn = psycopg2.connect(
        dbname='postgres',
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE "{dbname}";')
        print(f"Database '{dbname}' created.")
    else:
        print(f"Database '{dbname}' already exists.")
    cur.close()
    conn.close()

def run_table_creation(sql_file_path):
    """Run the table creation SQL using get_postgres_connection()."""
    conn = get_postgres_connection()
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    cur = conn.cursor()
    cur.execute(sql_script)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_database_if_not_exists()
    sql_file_path = '/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/SQL_files/capublic_Postgres2.sql'  # Update this path
    run_table_creation(sql_file_path)