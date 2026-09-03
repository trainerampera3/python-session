from fastapi import APIRouter

from database.connection  import get_connection

router = APIRouter(prefix="/orders_billing", tags=["orders_billing"])

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
                     "country",
                     
                """
            )
            rows = cursor.fetchall()
            # columns = [
            #     "order_billing _id",
            #     "name",
            #     "phone",
            #     "address_line1",
            #     "address_line2",
            #     "city",
            #     "state",
            #     "postal_code",
            #     "country"
            # ]
            # data = [dict(zip(columns, row)) for row in rows]
            # return {"count": len(data), "data": data}
            return {"count": len(rows), "data": rows}
    finally:
        connection.close()
        
        
# @router.post("")
# def create_discount(discount: dict):
#         connection = get_connection()

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     """
#                     INSERT INTO discounts (name, description, discount_percentage, start_date, end_date)
#                     VALUES (%s, %s, %s, %s, %s)
#                     RETURNING discount_id;
#                     """,
#                     (
#                         discount["name"],
#                         discount["description"],
#                         discount["discount_percentage"],
#                         discount["start_date"],
#                         discount["end_date"]
#                     )
#                 )
#                 new_discount_id = cursor.fetchone()[0]
#                 connection.commit()
#                 return {"message": "Discount created successfully", "discount_id": new_discount_id}
#         finally:
#             connection.close()
            
#             rows = cursor.fetchall()
#             columns = [
#                 "discount_id",
#                 "name",
#                 "description",
#                 "discount_percentage",
#                 "start_date",
#                 "end_date"
#             ]
#             data = [dict(zip(columns, row)) for row in rows]
#             return {"count": len(data), "data": data}
#     # finally:
#     #     connection.close()
        
        
# @router.post("")
# def create_discount(discount: dict):
#         connection = get_connection()

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     """
#                     INSERT INTO discounts (name, description, discount_percentage, start_date, end_date)
#                     VALUES (%s, %s, %s, %s, %s)
#                     RETURNING discount_id;
#                     """,
#                     (
#                         discount["name"],
#                         discount["description"],
#                         discount["discount_percentage"],
#                         discount["start_date"],
#                         discount["end_date"]
#                     )
#                 )
#                 new_discount_id = cursor.fetchone()[0]
#                 connection.commit()
#                 return {"message": "Discount created successfully", "discount_id": new_discount_id}
#         finally:
#             connection.close()