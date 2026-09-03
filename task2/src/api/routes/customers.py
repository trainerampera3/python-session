from fastapi import APIRouter

from database.connection  import get_connection

from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    gender: str
    customer_group_id: int
    status: str

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("")
def get_customers():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    email,
                    phone,
                    password,
                    gender,
                    customer_group_id,
                    status,
                    created_at,
                    updated_at 
                FROM customers
                ORDER BY name;
                """
            )
            rows = cursor.fetchall()
            columns = [
                "customer_id",
                "name",
                "email",
                "phone",
                "password",
                "gender",
                "customer_group_id",
                "status",
                "created_at",
                "updated_at"
            ]
            data = [dict(zip(columns, row)) for row in rows]
            return {"count": len(data), "data": data}
    finally:
        connection.close()
        
        
@router.post("")
def create_customer(customer: Customer):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers (name, email, phone, password, gender, customer_group_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING customer_id;
                    """,
                    (
                        customer.name,
                        customer.email,
                        customer.phone,
                        customer.password,
                        customer.gender,
                        customer.customer_group_id,
                        customer.status
                    )
                )
                new_customer_id = cursor.fetchone()[0]
                connection.commit()
                return {"message": "Customer created successfully", "customer_id": new_customer_id}
        finally:
            connection.close()
            
            
@router.get("/{customer_id}")
def get_customer(customer_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    email,
                    phone,
                    password,
                    gender,
                    customer_group_id,
                    status,
                    created_at,
                    updated_at
                FROM customers
                WHERE customer_id = %s;
                """,
                (customer_id,)
            )
            row = cursor.fetchone()
            if row:
                columns = [
                    "customer_id",
                    "name",
                    "email",
                    "phone",
                    "password",
                    "gender",
                    "customer_group_id",
                    "status",
                    "created_at",
                    "updated_at"
                ]
                data = dict(zip(columns, row))
                return {"data": data}
            else:
                return {"message": "Customer not found"}, 404
    finally:
        connection.close()
        
@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customers
                SET name = %s,
                    email = %s,
                    phone = %s,
                    password = %s,  
                    gender = %s,
                    customer_group_id = %s,
                    status = %s,
                    updated_at = NOW()
                WHERE customer_id = %s;
                """,
                (
                    customer.name,
                    customer.email,
                    customer.phone,
                    customer.password,
                    customer.gender,
                    customer.customer_group_id,
                    customer.status,
                    customer_id
                )
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": "Customer updated successfully"}
            else:
                return {"message": "Customer not found"}, 404
    finally:
        connection.close()
    
@router.delete("/{customer_id}")
def delete_customer(customer_id: int):  
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM customers
                WHERE customer_id = %s;
                """,
                (customer_id,)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": "Customer deleted successfully"}
            else:
                return {"message": "Customer not found"}, 404
    finally:
        connection.close()

@router.patch("/{customer_id}/status")
def update_customer_status(customer_id: int, status: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customers
                SET status = %s,
                    updated_at = NOW()
                WHERE customer_id = %s;
                """,
                (status, customer_id)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": "Customer status updated successfully"}
            else:
                return {"message": "Customer not found"}, 404
    finally:
        connection.close()
        
