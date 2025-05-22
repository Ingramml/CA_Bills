from Database_connection import get_postgres_connection
import psycopg2

def list_tables(schema='public'):
    """
    Returns a list of all table names in the specified PostgreSQL schema.
    Uses psycopg2 for the connection.
    """
    conn = get_postgres_connection()
    if conn is None:
        print("Could not establish database connection.")
        return []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name;
            """, (schema,))
            tables = [row[0] for row in cursor.fetchall()]
            return tables
    except psycopg2.Error as e:
        print(f"Error fetching tables: {e}")
        return []
    finally:
        conn.close()

# Example usage:
if __name__ == "__main__":
    tables = list_tables()
    print("Tables:", tables)