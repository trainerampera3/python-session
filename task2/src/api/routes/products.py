from fastapi import APIRouter , HTTPException

from pydantic import BaseModel
from database.connection import get_connection

class Products(BaseModel):
    prod_id: int
    name: str
    short_desc: str
    description: str
    specifications: dict
    additional_data: dict
    image_title: str
    image_url: str
    status: str
    created_at: str
    updated_at: str

router = APIRouter(prefix = "/products", tags=["Products"])

@router.get("")
def get_products():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
                        prod_id,
                        name,
                        short_desc,
                        description,
                        specifications,
                        additional_data,
                        image_title,
                        image_url,
                        status,
                        created_at,
                        updated_at
                    FROM products
                """
            )
            rows = cursor.fetchall()
            columns = [ "prod_id", "name", "short_desc", "description", "specifications", "additional_data", "image_title",
                        "image_url", "status", "created_at", "updated_at"]
            
            raw_data = [dict(zip(columns, row))for row in rows]

        return {"count" : len(raw_data), "data" : raw_data}

    finally:
        connection.close()

@router.get("/{prod_id}")
def get_prod_by_id(prod_id : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                  SELECT 
                    prod_id,
                    name,
                    short_desc,
                    description,
                    specifications,
                    additional_data,
                    image_title,
                    image_url,
                    status,
                    created_at,
                    updated_at
                  FROM products
                  WHERE prod_id = %s
                """,
                (prod_id,)
            )
            rows = cursor.fetchall()

            columns = [ "prod_id", "name", "short_desc", "description", "specifications", "additional_data", "image_title",
                        "image_url", "status", "created_at", "updated_at"]
            
            raw_data = [dict(zip(columns, row))for row in rows]

        return {"count" : len(raw_data), "data" : raw_data}

    finally:
        connection.close()


@router.get("/search/{name}")
def get_prod_by_name(name : str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                  SELECT 
                    prod_id,
                    name,
                    short_desc,
                    description,
                    specifications,
                    additional_data,
                    image_title,
                    image_url,
                    status,
                    created_at,
                    updated_at
                  FROM products
                  WHERE name = %s
                """,
                (name,)
            )
            rows = cursor.fetchall()
            columns = [ "prod_id", "name", "short_desc", "description", "specifications", "additional_data", "image_title",
                        "image_url", "status", "created_at", "updated_at"]
            raw_data = [dict(zip(columns, row))for row in rows]

        return {"count" : len(raw_data), "data" : raw_data}

    finally:
        connection.close()



@router.post("")
def create_product(product : Products):

    connection  = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO products (name, short_desc, description, specifications, additional_data, image_title, image_url, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING prod_id;        
                """,
                (
                    product.name,
                    product.short_desc,
                    product.description,
                    product.specifications,
                    product.additional_data,
                    product.image_title,
                    product.image_url,
                    product.status
                )
            )
            new_prod_id = cursor.fetchone()[0]
            connection.commit() 
            return {"messsage" : "Prodouct created successfuly","prod_id" : new_prod_id}

    finally:
        connection.close()

@router.put("/{prod_id}")
def update_product(prod_id : int, product : Products):  
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    UPDATE products
                    SET name = %s, short_desc = %s, description = %s, specifications = %s, additional_data = %s, image_title = %s, image_url = %s, status = %s,
                    updated_at = NOW()
                    WHERE prod_id = %s        
                """,
                (
                    product.name,
                    product.short_desc,
                    product.description,
                    product.specifications,
                    product.additional_data,
                    product.image_title,
                    product.image_url,
                    product.status,
                    prod_id
                )
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Product with ID {prod_id} updated successfully"}
            else:
                return {"message": f"Product with ID {prod_id} not found"}, 404

    finally:
        connection.close()


@router.patch("/{prod_id}")
def update_product_status(prod_id : int, status : str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    UPDATE products
                    SET status = %s,
                    updated_at = NOW()
                    WHERE prod_id = %s   
                """,
                (status, prod_id)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Product status with ID {prod_id} updated successfully"}
            else:
                return {"message": f"Product status with ID {prod_id} not found"}, 404

    finally:
        connection.close()  

@router.delete("/{prod_id}")   
def delete_product(prod_id : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DELETE From products
                    WHERE prod_id = %s      
                """,
                (prod_id,)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Product with ID {prod_id} deleted successfully",}
            else:
                return {"message": f"Product with ID {prod_id} not found"}, 404
    finally:
        connection.close()