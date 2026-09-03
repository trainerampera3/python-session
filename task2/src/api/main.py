from fastapi import FastAPI
from api.routes import customers

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(customers.router)    

    @app.get("/")
    def read_root():
        return {"message": "E-commerce API is running!"}

    return app

app = create_app()
