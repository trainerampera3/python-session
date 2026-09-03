from fastapi import FastAPI
from api.routes import customers
from task2.src.api.routes import orders_billing    

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)  
    app.include_router(orders_billing.router)  

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
