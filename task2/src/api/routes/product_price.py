from fastapi import APIRouter

from database.connection import get_connection
from pydantic import BaseModel , condecimal



class ProductPrice(BaseModel):
    prod_id: int
    price: condecimal(ge=0, decimal_places=2, max_digits=10) # type: ignore
    store_id: int

router = APIRouter(prefix = "/product_price", tags=["Product Price"])

@router.get("")
def get_product_price():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        prod_price_id,
                        prod_id,
                        price,
                        store_id
                    FROM product_price
                """
            )
            rows = cursor.fetchall()
            columns = ["prod_price_id", "prod_id", "price", "store_id"]
            raw_data = [dict(zip(columns, row)) for row in rows]
        return {"count": len(raw_data), "data": raw_data}
    finally:
        connection.close()


@router.get("/{prod_price_id}")
def get_product_price_by_id(prod_price_id : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        prod_price_id,
                        prod_id,
                        price,
                        store_id
                    FROM product_price
                    WHERE prod_price_id = %s
                """,
                (prod_price_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return {"message": "Product price not found"}
            columns = ["prod_price_id", "prod_id", "price", "store_id"]
            data = dict(zip(columns, row))
        return {"data": data}
    finally:
        connection.close()


@router.post("")
def create_product_price(product_price : ProductPrice):

    connection  = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO product_price (prod_id, price, store_id)
                    VALUES (%s, %s, %s)
                    RETURNING prod_price_id;               
                """,
                (
                    product_price.prod_id,
                    product_price.price,
                    product_price.store_id
                )
            )
            new_prod_price_id = cursor.fetchone()[0]
            connection.commit()
            return {"message": "Product price created successfully", "prod_price_id": new_prod_price_id}

    finally:
        connection.close()

@router.put("/{prod_price_id}")
def update_product_price(prod_price_id : int, product_price : ProductPrice):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO product_price (prod_price_id, prod_id, price, store_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING prod_price_id;        
                """,

            )

    finally:
        connection.close()


@router.patch("/{prod_price_id}")
def update_product_price_status(prod_price_id : int, price : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
                        
                """
            )

    finally:
        connection.close()

@router.delete("/{prod_price_id}")
def delete_product_price(prod_price_id : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DELETE FROM product_price
                    WHERE prod_price_id = %s           
                """,
                (prod_price_id,)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Product price with ID {prod_price_id} deleted successfully"}
            else:
                return {"message": f"Product price with ID {prod_price_id} not found"}, 404
    finally:
        connection.close()