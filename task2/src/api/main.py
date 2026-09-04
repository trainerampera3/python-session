from fastapi import FastAPI
from api.routes import customers , customers_group , customer_address
#Vinay
#sahir
from api.routes import orders, order_transactions
#Jhansi
#Deepika
from api.routes import orders_billing   

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)
    app.include_router(customers_group.router)
    app.include_router(customer_address.router)

    
    #Orders-Sahir
    
    
    
    

    #Orders2-Jayanth
    app.include_router(orders.router)
    app.include_router(order_transactions.router)
    
    
    
    
    #Orders3-Pushpa
    app.include_router(orders_billing.router)
    
    #products-Vinay
    
    
    
    
    #Stores-Deepika

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
