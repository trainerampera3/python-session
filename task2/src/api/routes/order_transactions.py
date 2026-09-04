from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_connection

router = APIRouter(prefix="/transacs", tags=['Transactions'])

class Trans(BaseModel):
    order_transaction_id:int
    order_id:int
    transaction_id:str
    amount:float
    status:str
    created_at:datetime

class transUpdate(BaseModel):
    order_id:int
    trans_id:str
    amount:float
    status:str
    
conn = get_connection()

@router.get("")
def get_order_trans():
    cur = conn.cursor()
    cur.execute('Select * from order_transactions;')
    rows = cur.fetchall()

    cols = [desc[0] for desc in cur.description]

    return [dict(zip(cols, row)) for row in rows]


@router.get('/{trans_id}')
def get_by_id(trans_id:int):
    cur = conn.cursor()
    cur.execute('select * from order_transactions where order_transaction_id = %s', (trans_id,))
    row = cur.fetchone()

    if row is None:
        return "No file found"

    cols = [desc[0] for desc in cur.description]
    return dict(zip(cols, row))


@router.post("")
def add_order_trans(trans:list[Trans]):
    cur =conn.cursor()
    for tran in trans:
        
        data = tran.model_dump()
        cols = ", ".join(data.keys())
        placeholders = ", ".join(['%s']*len(data))

        query = f"""Insert into order_transactions({cols}) values({placeholders})"""

        cur.execute(query, tuple(data.values(),))
    conn.commit()
    return {"message": "Inserted"}


@router.delete('/{trans_id}')
def delete_trans(trans_id:int):
    cur = conn.cursor()
    try:
        cur.execute('Delete from order_transactions where order_transaction_id = %s', (trans_id,))
        conn.commit()
        return 'Successfully Deleted'
    except Exception as e:
        return f"error occured {e}"





@router.put("/{trans_id}")
def update_order(trans_id: int, data: transUpdate):
    query = """update order_transactions set order_id = %s, transaction_id = %s, amount = %s, status= %s where order_transaction_id= %s"""
    values = (
        data.order_id,
        data.trans_id,
        data.amount,
        data.status,
        trans_id
    )
    try:
        cur=conn.cursor()

        cur.execute(query, values)
        conn.commit()
        return "Successfully updated"
    except Exception as e:
        return(f'Some Error {e}')


@router.patch('/{trans_id}')
def update_trans(trans_id:int, data:dict):
    cur = conn.cursor()
    try:
        cols = ", ".join([f'{key} = %s' for key in data.keys()])

        query = f"update order_transactions set {cols} where order_transaction_id = %s"

        vals = list(data.values())
        vals.append(trans_id)

        cur.execute(query,tuple(vals))
        conn.commit()

        return 'Successfully Updated'
    except Exception as e:
        return f"Some error occured ,{e}"
