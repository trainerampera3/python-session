from fastapi import FastAPI
from api.routes import customers , customers_group

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)    
    app.include_router(customers_group.router)

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
