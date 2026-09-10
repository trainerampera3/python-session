from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from database.connection import get_connection
from psycopg.types.json import Jsonb

router=APIRouter(
    prefix="/discounts",
    tags=["Discounts"]
)
conn =  get_connection()
class Discount(BaseModel):
    discount_id: int
    name: str
    description: str
    prod_ids: List[int]
    discount_type: str
    percentage: float
    coupon_code: str
    start_date: str
    end_date: str
    status: str
    created_at: str
    updated_at: str

class discountUpdate(BaseModel):
    name: str
    description: str
    prod_ids: List[int]
    discount_type: str
    percentage: float
    coupon_code: str
    status: str

@router.get("/discounts")
def get_discounts():
    cur = conn.cursor()
    cur.execute('Select *  from discounts')
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return [dict(zip(cols, row)) for row in rows]

@router.get("/discounts/{discount_id}")
def get_discount(discount_id: int):

    cur = conn.cursor()
    cur.execute('select * from discounts where discount_id = %s', (discount_id,))
    row = cur.fetchone()

    if row is None:
        return None

    cols = [desc[0] for desc in cur.description]
    return dict(zip(cols, row))
@router.post("/discounts")
def create_discount(discount: Discount):
    cur = conn.cursor()
    data = discount.model_dump()
    values = (
        discount.discount_id,
        discount.name,
        discount.description,
        Jsonb(discount.prod_ids),
        discount.discount_type,
        discount.percentage,
        discount.coupon_code,
        discount.start_date,
        discount.end_date,
        discount.status,
        discount.created_at,
        discount.updated_at
    )
    cols = ", ".join(data.keys())
    placeholders  = ", ".join(["%s"] * len(values))

    query = f"insert into discounts({cols}) values({placeholders})"

    cur.execute(query, tuple(values,))

    conn.commit()

    return {'inserted successfully'}

@router.put("/discounts/{discount_id}")
def update_discount(discount_id: int, discount: discountUpdate):

    query = """
        UPDATE discounts
        SET
            name = %s,
            description = %s,
            prod_ids = %s,
            discount_type = %s,
            percentage = %s,
            coupon_code = %s,
            status = %s,
            updated_at = NOW()
        WHERE discount_id = %s
    """

    values = (
        discount.name,
        discount.description,
        Jsonb(discount.prod_ids),
        discount.discount_type,
        discount.percentage,
        discount.coupon_code,
        discount.status,
        discount_id
    )

    try:
        cur = conn.cursor()
        cur.execute(query, values)

        if cur.rowcount == 0:
            conn.rollback()
            return "Discount not found"

        conn.commit()

        return "Successfully Updated"

    except Exception as e:
        conn.rollback()
        return f"Some error {e}"

    finally:
        cur.close()



@router.patch("/discounts/{discount_id}")
def patch_discount(discount_id: int,data:dict):
    cur = conn.cursor()
    try:
        cols = ", ".join(f"{key} = %s" for key in data.keys())
        values =list(data.values())
        values.append(discount_id)

        cur.execute(f'update discounts set {cols} where discount_id = %s',tuple(values))
        conn.commit()
        return f"successful"

    except Exception as e:
        print(f'Some error{e}')

@router.delete("/discounts/{discount_id}")
def delete_discount(discount_id: int):

    try:

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('delete from discounts where discount_id =%s',(discount_id,))
        conn.commit()
        return 'successdul'
    except:

        raise HTTPException(
            status_code=404,
            detail="Discount not found"
        )