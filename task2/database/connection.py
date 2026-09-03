# import psycopg

# connection = psycopg.connect(
#     host="localhost",
#     port=5433,
#     dbname="database_deepika",
#     user="deepika",
#     password="deepu1014"
# )

# print("Database connected successfully!")

# connection.close()

import psycopg
def get_connection():
    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="database_deepika",
        user="deepika",
        password="deepu1014"
    )

    return connection