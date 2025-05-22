#File checks to see if tables are already created
import os
import psycopg2

def tables_exist(conn, table_names, schema='public'):
    """Check if all tables in table_names exist in the PostgreSQL database."""
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(table_names))
    query = f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = %s AND table_name IN ({format_strings});
    """
    cursor.execute(query, [schema] + table_names)
    existing_tables = {row[0] for row in cursor.fetchall()}
    return all(table in existing_tables for table in table_names)

def run_create_tables(conn, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    cursor = conn.cursor()
    cursor.execute(sql_script)
    conn.commit()
    print("Tables created successfully.")

# Example usage:
if __name__ == "__main__":
    # Update these values with your actual database credentials
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port=5432
    )
    table_names = ['table1', 'table2', 'table3']  # Replace with your actual table names
    sql_file_path = '/Users/michaelingram/Documents/GitHub/CA_bills/CA_Bills/Sqlfiles/capublic.sql'
    if not tables_exist(conn, table_names):
        run_create_tables(conn, sql_file_path)
    else:
        print("All tables already exist.")
    conn.close()

