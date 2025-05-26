from Database_connection import get_postgres_connection
import os
from Python_automation.Dtablecreation import run_create_tables
from dotenv import load_dotenv


load_dotenv

conn=get_postgres_connection()
sql_dir = os.path.join(os.getcwd(), "Python_automation/SQL_files/capublic_Postgres2.sql")
#/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/SQL_files/capublic_BigQuery.sql
run_create_tables(conn, sql_dir)