from database.db_connection import db_conn


conn = db_conn()
cur = conn.cursor()


def create_orders(orders):

    for order in orders:

        data = order.model_dump()

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))

        query = f"""
        INSERT INTO orders ({columns})
        VALUES ({placeholders})
        """

        cur.execute(query, tuple(data.values()))

    conn.commit()

    return {"message": "Inserted"}