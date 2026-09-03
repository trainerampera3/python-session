from fastapi import APIRouter

from database.connection import get_connection

from pydantic import BaseModel

router = APIRouter(prefix="/customer_address", tags=["customer_address"])


class CustomerAddress(BaseModel):
    customer_address_id: int
    customer_id: int
    address_type: str
    address_line1: str
    address_line2: str
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool
    
    
@router.get("")
def get_customer_addresses():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_address_id,
                    customer_id,
                    address_type,
                    address_line1,
                    address_line2,
                    city,
                    state,
                    postal_code,
                    country,
                    is_default
                FROM customer_address
                ORDER BY customer_address_id;
                """
            )
            rows = cursor.fetchall()
            columns = [
                "customer_address_id",
                "customer_id",
                "address_type",
                "address_line1",
                "address_line2",
                "city",
                "state",
                "postal_code",
                "country",
                "is_default"
            ]
            data = [dict(zip(columns, row)) for row in rows]
            return {"count": len(data), "data": data}
    finally:
        connection.close()
        
@router.post("")
def create_customer_address(customer_address: CustomerAddress):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer_address (
                    customer_id,
                    address_type,
                    address_line1,
                    address_line2,
                    city,
                    state,
                    postal_code,
                    country,
                    is_default
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING customer_address_id;
                """,
                (
                    customer_address.customer_id,
                    customer_address.address_type,
                    customer_address.address_line1,
                    customer_address.address_line2,
                    customer_address.city,
                    customer_address.state,
                    customer_address.postal_code,
                    customer_address.country,
                    customer_address.is_default
                )
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return {"message": "Customer address created successfully", "customer_address_id": new_id}
    finally:
        connection.close()
        
@router.put("/{customer_address_id}")
def update_customer_address(customer_address_id: int, customer_address: CustomerAddress):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customer_address
                SET
                    customer_id = %s,
                    address_type = %s,
                    address_line1 = %s,
                    address_line2 = %s,
                    city = %s,
                    state = %s,
                    postal_code = %s,
                    country = %s,
                    is_default = %s,
                    updated_at = NOW()
                WHERE customer_address_id = %s;
                """,
                (
                    customer_address.customer_id,
                    customer_address.address_type,
                    customer_address.address_line1,
                    customer_address.address_line2,
                    customer_address.city,
                    customer_address.state,
                    customer_address.postal_code,
                    customer_address.country,
                    customer_address.is_default,
                    customer_address_id
                )
            )
            connection.commit()
            return {"message": "Customer address updated successfully"}
    finally:
        connection.close()
@router.delete("/{customer_address_id}")
def delete_customer_address(customer_address_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM customer_address
                WHERE customer_address_id = %s;
                """,
                (customer_address_id,)
            )
            connection.commit()
            return {"message": "Customer address deleted successfully"}
    finally:
        connection.close()
@router.get("/{customer_address_id}")
def get_customer_address(customer_address_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_address_id,
                    customer_id,
                    address_type,
                    address_line1,
                    address_line2,
                    city,
                    state,
                    postal_code,
                    country,
                    is_default
                FROM customer_address
                WHERE customer_address_id = %s;
                """,
                (customer_address_id,)
            )
            row = cursor.fetchone()
            if row:
                columns = [
                    "customer_address_id",
                    "customer_id",
                    "address_type",
                    "address_line1",
                    "address_line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "is_default"
                ]
                data = dict(zip(columns, row))
                return {"data": data}
            else:
                return {"message": "Customer address not found"}, 404
    finally:
        connection.close()