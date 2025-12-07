from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.jokes_controller import router as jokes_router

def register_routes(app: FastAPI):
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(jokes_router, prefix="/jokes", tags=["Jokes"])
