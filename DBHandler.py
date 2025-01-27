import psycopg2 as pg  

def TableSetup (connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS GoStorage (
                id SERIAL PRIMARY KEY,
                pokemon_name VARCHAR(50),
                storage_location VARCHAR(100)
            );
            """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    TableSetup()