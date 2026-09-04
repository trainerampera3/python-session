from fastapi import APIRouter
from pydantic import BaseModel
from database.connection  import get_connection

class OrderBilling(BaseModel):
    order_billing_id: int
    order_id: int
    name: str
    phone: str
    address_line1: str
    address_line2: str
    city: str
    state: str
    postal_code: str
    country: str

router = APIRouter(prefix="/order_billing", tags=["orders_billing"])

@router.get("")
def get_orders_billing():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                     "order_billing_id",
                    "order_id",
                   "name",
                    "phone",
                        "address_line1",
                     "address_line2",
                     "city",
                     "state",
                     "postal_code",
                     "country"
                     FROM order_billing
                     ORDER BY "order_billing_id";
                     
                """
            )
            
            rows = cursor.fetchall()
            return {"count": len(rows), "data": rows}
    finally:
        connection.close()
        
        
@router.post("")
def create_order_billing(order: OrderBilling):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO order_billing (order_id, name, phone, address_line1, address_line2, city, state, postal_code, country)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING order_billing_id;
                    """,
                    (
                        order.order_billing_id,
                        order.order_id,
                        order.name,
                        order.phone,
                        order.address_line1,
                        order.address_line2,
                        order.city,
                        order.state,
                        order.postal_code,
                        order.country
                    )
                )
                new_order_billing_id = cursor.fetchone()[0]
                connection.commit()
                return {"message": "Order billing created successfully", "order_billing_id": new_order_billing_id}
        finally:
            connection.close()

@router.put("/{order_billing_id}")
def update_order_billing(order_billing_id: int, order: OrderBilling):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE order_billing
                SET order_id = %s,
                    name = %s,
                    phone = %s,
                    address_line1 = %s,
                    address_line2 = %s,
                    city = %s,
                    state = %s,
                    postal_code = %s,
                    country = %s
                WHERE order_billing_id = %s;
                """,
                (
                    order.order_id,
                    order.name,
                    order.phone,
                    order.address_line1,
                    order.address_line2,
                    order.city,
                    order.state,
                    order.postal_code,
                    order.country,
                    order_billing_id
                )
            )
            connection.commit()
            return {"message": "Order billing updated successfully"}
    finally:
        connection.close()
        
@router.delete("/{order_billing_id}")
def delete_order_billing(order_billing_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM order_billing
                WHERE order_billing_id = %s;
                """,
                (order_billing_id,)
            )
            connection.commit()
            return {"message": "Order billing deleted successfully"}
    finally:
        connection.close()

@router.patch("/{order_billing_id}")
def update_order_billing_phone(order_billing_id: int, phone: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE order_billing
                SET phone = %s
                WHERE order_billing_id = %s;
                """,
                (phone, order_billing_id)
            )

            connection.commit()

            return {
                "message": "Phone updated successfully",
                "order_billing_id": order_billing_id,
                "phone": phone
            }

    finally:
        connection.close()