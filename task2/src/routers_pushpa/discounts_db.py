import os
import psycopg





def get_connection():
    return psycopg.connect(
        host=("localhost"),
        port=("5433"),
        dbname=("Ecommerce_db"),
        user=("pushpa"),
        password=("pushpa")
    )

connection = get_connection()
print("Connection established successfully!")
connection.close()