#File checks to see if tables are already created
import os

def run_create_tables(conn, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    cursor = conn.cursor()
    # Split on semicolon to handle multiple statements
    for statement in sql_script.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()
    print("Tables created successfully.")

# Example usage:
# from your_db_module import get_connection
# conn = get_connection()
# run_create_tables(conn, '/path/to/your/capublic.sql')

query_location='/Users/michaelingram/Documents/GitHub/CA_bills/CA_Bills/Sqlfiles/capublic.sql'

