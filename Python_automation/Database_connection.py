import psycopg2
import os
from dotenv import load_dotenv

def get_postgres_connection():
    """
    Create and return a PostgreSQL database connection using psycopg2.
    Loads credentials from environment variables.
    """
    load_dotenv()  # Load variables from .env file

    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)
    
    print(f"Connecting to database {dbname} at {host}:{port} as user {user}")
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Database connection established.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
    

get_postgres_connection()