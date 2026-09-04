from api.routes.signup import router as signup_router

from api.routes.login import router as login_router

from fastapi import FastAPI



def create_app() -> FastAPI:
    app = FastAPI()
    
    
    app.include_router(signup_router)
    
    app.include_router(login_router)
    
    
    
    return app



app = create_app()