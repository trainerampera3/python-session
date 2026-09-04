from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.connection import get_connection
conn=get_connection()

router = APIRouter(prefix="/order_shipping", tags=["order_shipping"])

class Ordershipping(BaseModel):
    order_id: int
    name: str | None = None
    phone: str | None = None
    address_line1: str
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    shipping_method: str | None = None
    shipping_cost: Decimal = 0
    tracking_number: str | None = None
    status: str | None = None

@router.get('/fetch_details')
def fetch_details():
    res=None
    with conn.cursor() as cur:
        cur.execute("select * from order_shipping limit 10")
        res=cur.fetchall()
    return {
        'data':res
    }
@router.post('/insert_details')
def insert_details(order_shipping_input: Ordershipping):

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO order_shipping (
                order_id,
                name,
                phone,
                address_line1,
                address_line2,
                city,
                state,
                postal_code,
                country,
                shipping_method,
                shipping_cost,
                tracking_number,
                status
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            RETURNING order_shipping_id;
        """, (
            order_shipping_input.order_id,
            order_shipping_input.name,
            order_shipping_input.phone,
            order_shipping_input.address_line1,
            order_shipping_input.address_line2,
            order_shipping_input.city,
            order_shipping_input.state,
            order_shipping_input.postal_code,
            order_shipping_input.country,
            order_shipping_input.shipping_method,
            order_shipping_input.shipping_cost,
            order_shipping_input.tracking_number,
            order_shipping_input.status
        ))

        order_shipping_id = cur.fetchone()[0]

    conn.commit()

    return {
        "message": "Shipping details inserted successfully",
        "order_shipping_id": order_shipping_id,
        "data": order_shipping_input
    }

@router.put('/update_details/{order_shipping_id}')
def update_details(order_shipping_id: int, update_details: Ordershipping):

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE order_shipping
            SET
                order_id = %s,
                name = %s,
                phone = %s,
                address_line1 = %s,
                address_line2 = %s,
                city = %s,
                state = %s,
                postal_code = %s,
                country = %s,
                shipping_method = %s,
                shipping_cost = %s,
                tracking_number = %s,
                status = %s
            WHERE order_shipping_id = %s
        """, (
            update_details.order_id,
            update_details.name,
            update_details.phone,
            update_details.address_line1,
            update_details.address_line2,
            update_details.city,
            update_details.state,
            update_details.postal_code,
            update_details.country,
            update_details.shipping_method,
            update_details.shipping_cost,
            update_details.tracking_number,
            update_details.status,
            order_shipping_id
        ))

    conn.commit()

    return {
        "message": "Shipping details updated successfully"
    }
@router.patch('/update_status/{col_name}/{value}/{order_shipping_id}')
def partial_update_status(col_name: str, value: str, order_shipping_id: int):
    with conn.cursor() as cur:
        query = f"UPDATE order_shipping SET {col_name} = %s WHERE order_shipping_id = %s"
        cur.execute(query, (value, order_shipping_id))
    conn.commit()
    return {
        "message": f"{col_name} updated successfully for order_shipping_id {order_shipping_id}"
    }

@router.delete('/delete_details/{order_shipping_id}')
def delete_details(order_shipping_id: int):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM order_shipping WHERE order_shipping_id = %s", (order_shipping_id,))
    conn.commit()
    return {
        "message": f"Shipping details deleted successfully for order_shipping_id {order_shipping_id}"
    }

