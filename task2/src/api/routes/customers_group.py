from fastapi import APIRouter, Depends
from database.connection import get_connection
from pydantic import BaseModel

class CustomerGroup(BaseModel):
    customer_group_id: int
    name: str
    status: str
    
router = APIRouter(prefix="/customers_group", tags=["customers_group"])

@router.get("")
def get_customers_group():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_group_id,
                    name,
                    status
                FROM customer_group
                ORDER BY name;
                """
            )
            rows = cursor.fetchall()
            columns = [
                "customer_group_id",
                "name",
                "status"
            ]
            data = [dict(zip(columns, row)) for row in rows]
            return {"count": len(data), "data": data}
    finally:
        connection.close()
        
@router.post("")
def create_customer_group(customer_group: CustomerGroup):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer_group (name, status)
                VALUES (%s, %s)
                RETURNING customer_group_id;
                """,
                (customer_group.name, customer_group.status)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return {"message": "Customer group created successfully", "customer_group_id": new_id}
    finally:
        connection.close()

@router.put("/{customer_group_id}")
def update_customer_group(customer_group_id: int, customer_group: CustomerGroup):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customer_group
                SET name = %s, status = %s, updated_at = NOW()
                WHERE customer_group_id = %s;
                """,
                (customer_group.name, customer_group.status, customer_group_id)
            )
            connection.commit()
            return {"message": "Customer group updated successfully"}
    finally:
        connection.close()


@router.delete("/{customer_group_id}")
def delete_customer_group(customer_group_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM customer_group
                WHERE customer_group_id = %s;
                """,
                (customer_group_id,)
            )
            connection.commit()
            return {"message": "Customer group deleted successfully"}
    finally:
        connection.close()
        
@router.get("/{customer_group_id}")
def get_customer_group(customer_group_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_group_id,
                    name,
                    status
                FROM customer_group
                WHERE customer_group_id = %s;
                """,
                (customer_group_id,)
            )
            row = cursor.fetchone()
            if row:
                columns = [
                    "customer_group_id",
                    "name",
                    "status"
                ]
                data = dict(zip(columns, row))
                return {"data": data}
            else:
                return {"message": "Customer group not found"}
    finally:
        connection.close()
        
@router.patch("/{customer_group_id}")
def update_customer_group_status(customer_group_id: int, status: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customer_group
                SET status = %s, updated_at = NOW()
                WHERE customer_group_id = %s;
                """,
                (status, customer_group_id)
            )
            connection.commit()
            return {"message": "Customer group status updated successfully"}
    finally:
        connection.close()