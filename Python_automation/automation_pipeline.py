#from filedownload import download_pubinfo_daily_sun
from movefiles import unzip,move_files
from Database_connection import get_postgres_connection
import os
from dotenv import load_dotenv
from loadData2 import load_sql_files
from filedownload_3 import download_pubinfo_files



output_folder = current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir) 
working_dir,zipfile_path=download_pubinfo_files(output_folder)
print(f"Zip file path: {zipfile_path}")
print(f"Working directory: {working_dir}")
zipdir=unzip(*zipfile_path)
move_files(*zipdir)
load_dotenv()
conn=get_postgres_connection
sql_dir="/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/SQL_files/Executes_Postgres"
data_dir= os.path.join(working_dir, "bat_files")
load_sql_files(sql_dir,data_dir,)
