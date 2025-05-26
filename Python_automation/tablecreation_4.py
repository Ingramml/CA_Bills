import os
import psycopg2
from dotenv import load_dotenv
import re

def get_existing_tables(schema, table_names):
    """
    Checks which tables from table_names already exist in the given schema.
    Returns a set of existing table names.
    """
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
    format_strings = ','.join(['%s'] * len(table_names))
    query = f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = %s AND table_name IN ({format_strings});
    """
    cur.execute(query, [schema] + table_names)
    existing = {row[0] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return existing

def parse_table_names_from_sql(sql_file_path, schema):
    """
    Parses the SQL file to find all tables that will be created in the given schema.
    Returns a list of table names.
    """
    table_names = []
    pattern = re.compile(rf'CREATE\s+TABLE\s+{schema}\.([a-zA-Z0-9_]+)', re.IGNORECASE)
    with open(sql_file_path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                table_names.append(match.group(1))
    return table_names

def run_sql_file_with_check(sql_file_path, schema):
    """
    Checks if any tables to be created already exist in the schema.
    Warns the user and prompts for confirmation before running the SQL file.
    """
    table_names = parse_table_names_from_sql(sql_file_path, schema)
    if not table_names:
        print("No CREATE TABLE statements found in the SQL file.")
        return
    existing = get_existing_tables(schema, table_names)
    if existing:
        print(f"Warning: The following tables already exist in schema '{schema}': {', '.join(existing)}")
        proceed = input("Do you want to continue and potentially overwrite these tables? (yes/no): ")
        if proceed.strip().lower() != "yes":
            print("Aborting execution.")
            return
    run_sql_file(sql_file_path)

def run_sql_file(sql_file_path):
    """
    Executes all SQL statements in the given file on the database specified by environment variables.
    Loads credentials from .env, connects to the database, runs the SQL, and commits the transaction.
    Prints a success message or error if execution fails.
    """
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
    """
    Connects to the database using credentials from .env and prints all tables and their schemas.
    Useful for verifying what tables exist and in which schema after running a SQL script.
    """
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
    schema = "capublic"
    run_sql_file_with_check(sql_file_path, schema)
    list_tables_and_schemas()