from fastapi import FastAPI
from api.routes import customers , customers_group , customer_address
#Vinay
#sahir
#Jay
#Jhansi
#Deepika
#Pushpa

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)
    app.include_router(customers_group.router)
    app.include_router(customer_address.router)
    
    #Orders-Sahir
    
    
    
    

    #Orders2-Jayanth
    
    
    
    
    #Orders3-Pushpa
    
    
    #products-Vinay
    
    
    
    
    #Stores-Deepika

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
