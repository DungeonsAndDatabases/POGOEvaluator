import os
import requests
import psycopg2 as pg
from DBHandler import TableSetup
# indirectly using credentials as strings from environment variables for security
dbname = os.environ['DB_NAME']
user = os.environ['postgreSQL_USER']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']

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
