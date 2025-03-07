import os
#dbname = os.environ['DB_NAME']

import psycopg2 as pg
from DBHandler import TableSetup
# Directly using credentials as strings
dbname = "ahuehuete_pc"
user = "postgres"
password = os.environ['DB_PASSWORD']
host = "localhost"
port = "5432"

try:
    print("Attempting to connect to the default database...")
    connection = pg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connection etablished")
    TableSetup (connection)
    connection.close()
except pg.OperationalError as e:
    print("Failed to connect to the database.")
    print(f"Error: {e}")
except UnicodeDecodeError as e:
    print("Unicode decode error occurred.")
    print(f"Error: {e}")
    print(f"Problematic string position: {e.start} to {e.end}")
except Exception as e:
    print("An unexpected error occurred.")
    print(f"Error: {e}")
