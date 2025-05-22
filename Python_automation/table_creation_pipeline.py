from Database_connection import get_postgres_connection
import os
from tablecreation import run_create_tables
from dotenv import load_dotenv

load_dotenv

conn=get_postgres_connection()
run_create_tables(conn, '/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation/SQL_files/capublic_Postgres2.sql')