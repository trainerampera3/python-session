import psycopg as pg 
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    try:
        connection = pg.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Exception as exc:  
        print(f"Connection error: {exc}")
        return None
