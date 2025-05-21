#From Chatgpt
# This script converts a MySQL SQL file to PostgreSQL and BigQuery compatible SQL files.
# It reads the original MySQL SQL file, applies necessary transformations, and saves the converted files.
from pathlib import Path

# Load the original MySQL SQL content
mysql_sql_path = Path("/mnt/data/capublic.sql")
mysql_sql_content = mysql_sql_path.read_text()

# Helper function to replace MySQL-specific syntax with PostgreSQL-compatible syntax
def convert_to_postgres(sql):
    sql = sql.replace("`", "\"")
    sql = sql.replace("ENGINE = INNODB", "")
    sql = sql.replace("CHARACTER SET utf8 COLLATE utf8_general_ci", "")
    sql = sql.replace("DATETIME", "TIMESTAMP")
    sql = sql.replace("LONGBLOB", "BYTEA")
    sql = sql.replace("LONGTEXT", "TEXT")
    sql = sql.replace("DECIMAL", "NUMERIC")
    sql = sql.replace("INT(", "INTEGER(")
    sql = sql.replace("INT(2)", "SMALLINT")
    sql = sql.replace("INT(3)", "SMALLINT")
    sql = sql.replace("INT(4)", "INTEGER")
    sql = sql.replace("INT(5)", "INTEGER")
    sql = sql.replace("INT(8)", "BIGINT")
    sql = sql.replace("IF NOT EXISTS", "")  # PostgreSQL does not support this in CREATE DATABASE
    sql = sql.replace("USE \"capublic\";", "")  # No USE statement in PostgreSQL
    sql = sql.replace("SET FOREIGN_KEY_CHECKS = 0;", "")
    sql = sql.replace("SET FOREIGN_KEY_CHECKS = 1;", "")
    sql = sql.replace("GRANT ALL ON capublic.* TO capublic@'%' IDENTIFIED BY 'capublic';", "")
    return sql

# Helper function to replace MySQL-specific syntax with BigQuery-compatible syntax
def convert_to_bigquery(sql):
    sql = sql.replace("`", "")
    sql = sql.replace("ENGINE = INNODB", "")
    sql = sql.replace("CHARACTER SET utf8 COLLATE utf8_general_ci", "")
    sql = sql.replace("DATETIME", "DATETIME")
    sql = sql.replace("LONGBLOB", "BYTES")
    sql = sql.replace("LONGTEXT", "STRING")
    sql = sql.replace("VARCHAR", "STRING")
    sql = sql.replace("DECIMAL", "NUMERIC")
    sql = sql.replace("INT(", "INT64(")
    sql = sql.replace("INT(2)", "INT64")
    sql = sql.replace("INT(3)", "INT64")
    sql = sql.replace("INT(4)", "INT64")
    sql = sql.replace("INT(5)", "INT64")
    sql = sql.replace("INT(8)", "INT64")
    sql = sql.replace("IF NOT EXISTS", "")
    sql = sql.replace("USE capublic;", "")
    sql = sql.replace("SET FOREIGN_KEY_CHECKS = 0;", "")
    sql = sql.replace("SET FOREIGN_KEY_CHECKS = 1;", "")
    sql = sql.replace("GRANT ALL ON capublic.* TO capublic@'%' IDENTIFIED BY 'capublic';", "")
    return sql

# Convert SQL to PostgreSQL
postgres_sql = convert_to_postgres(mysql_sql_content)

# Convert SQL to BigQuery
bigquery_sql = convert_to_bigquery(mysql_sql_content)

# Save both converted SQL files
postgres_path = "/mnt/data/capublic_Postgres.sql"
bigquery_path = "/mnt/data/capublic_BigQuery.sql"

Path(postgres_path).write_text(postgres_sql)
Path(bigquery_path).write_text(bigquery_sql)

postgres_path, bigquery_path
