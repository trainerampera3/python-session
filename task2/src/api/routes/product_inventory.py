from fastapi import APIRouter

from database.connection import get_connection

from pydantic import BaseModel,Field

class ProductInventory(BaseModel):
    prod_id: int
    quantity: int = Field(ge=0 ,default=0 , description="Quantity must be a non-negative integer")
    store_id: int

router = APIRouter(prefix = "/product_inventory", tags=["Product Inventory"])

@router.get("")
def get_product_inventory():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        prod_inv_id,
                        prod_id,
                        quantity,
                        store_id
                    FROM product_inventory
                """
            )
            rows = cursor.fetchall()
            columns = ["prod_inv_id", "prod_id", "quantity", "store_id"]

            raw_data = [dict(zip(columns, row)) for row in rows]

        return {"count": len(raw_data), "data": raw_data}
    
    finally:
        connection.close()      


@router.get("/{prod_inv_id}")
def get_product_inventory_by_id(prod_inv_id : int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        prod_inv_id,
                        prod_id,
                        quantity,
                        store_id
                    FROM product_inventory
                    WHERE prod_inv_id = %s
                """,
                (prod_inv_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return {"message": "Product inventory not found"}
            
            columns = ["prod_inv_id", "prod_id", "quantity", "store_id"]
            data = dict(zip(columns, row))
            return {"data": data}
    
    finally:
        connection.close()


@router.post("")
def create_product_inventory(product_inventory : ProductInventory):
    connection  = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO product_inventory (prod_id, quantity, store_id) 
                    VALUES (%s, %s, %s)
                    Returning prod_inv_id;           
                """,
                (
                    product_inventory.prod_id,
                    product_inventory.quantity,
                    product_inventory.store_id
                )
            )
            new_prod_inv_id = cursor.fetchone()[0]
            connection.commit()
            return {"message": "Product inventory created successfully", "prod_inv_id": new_prod_inv_id}
    
    finally:
        connection.close()   


@router.put("/{prod_inv_id}")
def update_product_inventory(prod_inv_id : int, product_inventory : ProductInventory):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
    
    
                            
                """
            )
        return 2
    
    finally:
        connection.close()


@router.patch("/{prod_inv_id}")
def update_product_inventory_quantity(prod_inv_id : int, quantity : int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
    
    
                            
                """
            )
        return 2
    
    finally:
        connection.close()


@router.delete("/{prod_inv_id}")
def delete_product_inventory(prod_inv_id : int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DELETE FROM product_inventory
                    WHERE prod_inv_id = %s             
                """,
                (prod_inv_id,)
            )
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Product inventory with ID {prod_inv_id} deleted successfully"}
            else:
                return {"message": f"Product inventory with ID {prod_inv_id} not found"}, 404  
    
    finally:
        connection.close()