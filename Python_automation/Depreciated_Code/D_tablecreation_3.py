import os
import psycopg2
from dotenv import load_dotenv

def run_sql_file(sql_file_path):
    # Load environment variables
    load_dotenv()
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)

    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()
    try:
        with open(sql_file_path, "r") as f:
            sql = f.read()
        cur.execute(sql)
        conn.commit()
        print(f"Executed {sql_file_path} successfully.")
    except Exception as e:
        print(f"Error executing {sql_file_path}: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def list_tables_and_schemas():
    load_dotenv()
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()
    print(f"\nTables in database '{dbname}':")
    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name;
    """)
    rows = cur.fetchall()
    for schema, table in rows:
        print(f"Schema: {schema}, Table: {table}")
    cur.close()
    conn.close()

# Example usage:
if __name__ == "__main__":
    sql_file_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/SQL_files/capublic_Postgres2.sql"
    run_sql_file(sql_file_path)
    list_tables_and_schemas()