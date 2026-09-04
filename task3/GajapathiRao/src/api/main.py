from api.routes.signup import router as signup_router

from fastapi import FastAPI



def create_app() -> FastAPI:
    app = FastAPI()
    
    
    app.include_router(signup_router)
    
    
    
    return app



app = create_app()