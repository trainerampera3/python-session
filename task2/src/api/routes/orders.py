from fastapi import APIRouter
router = APIRouter(prefix="/oders", tags=["Orders"])
from pydantic import BaseModel
from datetime import datetime
from database.connection import get_connection


conn = get_connection()
cur =conn.cursor()

class Order(BaseModel):
    order_id: int
    customer_id: int
    store_id: int
    base_price: float
    sub_total: float
    tax: float
    grand_total: float
    discount: float
    payment_type: str
    status: str
    created_at: datetime
    updated_at: datetime



@router.get("/orders")
def get_orders():
    with conn.cursor() as cur:
        cur.execute('select * from orders')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        return [dict(zip(columns,row)) for row in rows]


@router.post("/orders")
def add_order(orders:list[Order]):

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


@router.get("/orders/{order_id}")
def get_order(order_id:int):
    cur.execute('SELECT * FROM orders WHERE order_id = %s', (order_id,))
    row = cur.fetchone()
   
    if row is None:
        return None
   
    columns = [desc[0] for desc in cur.description]
    return dict(zip(columns, row))


@router.patch('/orders/{order_id}')
def update_orders(order_id:int,data:dict):
    try:
        columns = ", ".join([f"{key} = %s " for key in data.keys()])

        query = f"""Update orders set {columns} where order_id = %s"""

        values = list(data.values())
        values.append(order_id)

        cur.execute(query, tuple(values))
        conn.commit()

        return {"message": "Order updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.delete('/orders/{order_id}')
def delete_order(order_id:int):
    try:
        cur.execute('Delete from order where order_id = %s',(order_id,))
        deleted = cur.fetchone()
        if not deleted:
            raise Exception
    except Exception as e:
        print(f'No such file or data Existed {e}')



@router.put('/orders/{order_id}')
def insert_order(order_id:int, )