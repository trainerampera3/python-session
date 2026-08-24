import psycopg

def create_connection():
    try:
        connection = psycopg.connect(
            host="localhost",
            dbname="postgres",
            user="gajapathi",
            password="admin@123"
        )
        print("Connection to the database established successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

create_connection()