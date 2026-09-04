from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_connection

router = APIRouter(prefix="/orders", tags=["Orders"])


conn = get_connection()

class OrderUpdate(BaseModel):
    cust_id: int
    store_id: int
    base_price: float
    sub_total: float
    tax: float
    grand_total: float
    discount: float
    payment_type: str
    status: str


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



@router.get("")
def get_orders():
    with conn.cursor() as cur:
        cur.execute('select * from orders')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        return [dict(zip(columns,row)) for row in rows]


@router.post("")
def add_order(orders:list[Order]):

    for order in orders:
        cur =conn.cursor()

        data = order.model_dump()

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))

        query = f"""
        INSERT INTO orders ({columns})
        VALUES ({placeholders})
        """

        cur.execute(query, tuple(data.values(),))

    conn.commit()

    return {"message": "Inserted"}


@router.get("/{order_id}")
def get_order(order_id:int):
    cur =conn.cursor()
    cur.execute('SELECT * FROM orders WHERE order_id = %s', (order_id,))
    row = cur.fetchone()
   
    if row is None:
        return None
   
    columns = [desc[0] for desc in cur.description]
    return dict(zip(columns, row))


@router.patch('/{order_id}')
def update_orders(order_id:int,data:dict):
    cur =conn.cursor()
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


@router.delete('/{order_id}')
def delete_order(order_id:int):
    cur =conn.cursor()
    try:
        cur.execute('Delete from orders where order_id = %s',(order_id,))
        deleted = cur.fetchone()
        if not deleted:
            raise Exception
        return 'successfully removed'
    except Exception as e:
        print(f'No such file or data Existed {e}')


@router.put("/{order_id}")
def update_order(order_id: int, data: OrderUpdate):
    query = """update orders set customer_id = %s, store_id = %s, base_price = %s, sub_total= %s, tax = %s, grand_total=%s, discount = %s,  payment_type= %s, status= %s, updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata' where order_id = %s"""
    values = (
        data.cust_id,
        data.store_id,
        data.base_price,
        data.sub_total,
        data.tax,
        data.grand_total,
        data.discount,
        data.payment_type,
        data.status,
        order_id
    )
    try:
        cur=conn.cursor()

        cur.execute(query, values)
        conn.commit()
        return "Successfully updated"
    except Exception as e:
        return(f'Some Error {e}')
    


