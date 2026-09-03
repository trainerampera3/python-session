from fastapi import FastAPI
from api.routes import customers , customers_group , customer_address
#Vinay
from api.routes import order_items,order_shipping
#Jay
#Jhansi
from api.routes import stores
from api.routes import orders_billing   

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)
    app.include_router(customers_group.router)
    app.include_router(customer_address.router)
    #Orders-Sahir
    app.include_router(order_items.router)
    app.include_router(order_shipping.router)
    
    
    
    
    

    #Orders2-Jayanth
    
    
    
    
    #Orders3-Pushpa
    app.include_router(orders_billing.router)
    
    #products-Vinay
    
    
    
    
    #Stores-Deepika
    app.include_router(stores.router)

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
