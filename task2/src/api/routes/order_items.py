from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.connection import get_connection
conn = get_connection()
router = APIRouter(prefix="/order_items", tags=["order_items"])


class OrderItems(BaseModel):
    order_id: int
    prod_id: int
    quantity: int
    unit_price: Decimal
    sub_total: Decimal


# GET
@router.get('/fetch_order_items')
def fetch_order_items():
    res = None

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM order_items LIMIT 10")
        res = cur.fetchall()

    return {
        'data': res
    }


# POST
@router.post('/insert_order_item')
def insert_order_item(order_item_input: OrderItems):

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO order_items (
                order_id,
                prod_id,
                quantity,
                unit_price,
                sub_total
            )
            VALUES (
                %s, %s, %s, %s, %s
            )
            RETURNING order_item_id;
        """, (
            order_item_input.order_id,
            order_item_input.prod_id,
            order_item_input.quantity,
            order_item_input.unit_price,
            order_item_input.sub_total
        ))

        order_item_id = cur.fetchone()[0]

    conn.commit()

    return {
        "message": "Order item inserted successfully",
        "order_item_id": order_item_id,
        "data": order_item_input
    }


# PUT
@router.put('/update_order_item/{order_item_id}')
def update_order_item(
    order_item_id: int,
    update_order_item: OrderItems
):

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE order_items
            SET
                order_id = %s,
                prod_id = %s,
                quantity = %s,
                unit_price = %s,
                sub_total = %s
            WHERE order_item_id = %s
        """, (
            update_order_item.order_id,
            update_order_item.prod_id,
            update_order_item.quantity,
            update_order_item.unit_price,
            update_order_item.sub_total,
            order_item_id
        ))

    conn.commit()

    return {
        "message": "Order item updated successfully"
    }


# PATCH
@router.patch('/update_order_item/{col_name}/{value}/{order_item_id}')
def partial_update_order_item(
    col_name: str,
    value: str,
    order_item_id: int
):

    with conn.cursor() as cur:
        query = f"""
            UPDATE order_items
            SET {col_name} = %s
            WHERE order_item_id = %s
        """

        cur.execute(query, (value, order_item_id))

    conn.commit()

    return {
        "message": f"{col_name} updated successfully for order_item_id {order_item_id}"
    }


# DELETE
@router.delete('/delete_order_item/{order_item_id}')
def delete_order_item(order_item_id: int):

    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM order_items WHERE order_item_id = %s",
            (order_item_id,)
        )

    conn.commit()

    return {
        "message": f"Order item deleted successfully for order_item_id {order_item_id}"
    }