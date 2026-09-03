from fastapi import APIRouter

from database.connection import get_connection

router = APIRouter(prrefix = "/products", tags=["Products"])

@router.get("")
def get_products():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.excute(
                """
                    SELECT 

                """
            )
        a=10
        return a

    finally:
        connection.close()



@router.post("")
def create_product(customer : dict):

    connection  = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.excute(
                """
                    SELECT
                        
                """
            )

    finally:
        connection.close()