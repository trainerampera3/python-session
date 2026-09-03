from database.db_connection import db_conn

conn = db_conn()

def get_orders():
    with conn.cursor() as cur:
        cur.execute('select * from orders')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        return [dict(zip(columns,row)) for row in rows]
        