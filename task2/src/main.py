from fastapi import FastAPI
from fastapi import Body
from routers.get_orders import get_orders
from routers.add_orders import create_orders

from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    order_id: int
    customer_id: int
    store_id: int
    base_price: float
    sub_total: float
    tax: float
    grand_total: float
    discount: float
    payment_type: str
    status: str
    created_at: datetime
    updated_at: datetime



app = FastAPI()

@app.get("/orders")
def home():
    return get_orders()



@app.post("/orders")
def add_order(data:list[Order]):
    return create_orders(data)