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