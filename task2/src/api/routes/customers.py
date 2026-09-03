from fastapi import APIRouter

from database.connection  import get_connection

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
def create_customer(customer: dict):
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
                        customer["name"],
                        customer["email"],
                        customer["phone"],
                        customer["password"],
                        customer["gender"],
                        customer["customer_group_id"],
                        customer["status"]
                    )
                )
                new_customer_id = cursor.fetchone()[0]
                connection.commit()
                return {"message": "Customer created successfully", "customer_id": new_customer_id}
        finally:
            connection.close()