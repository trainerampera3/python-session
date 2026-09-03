import psycopg as pg

def db_conn():
    return pg.connect(
        dbname='ecommerce',
        user='jayanth',
        password='admin@123',
        port=5433,
        host='localhost'
    )