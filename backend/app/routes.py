from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.jokes_controller import router as jokes_router
from app.controllers.user_controller import router as user_router
from app.controllers.chat_controller import router as chat_router

def register_routes(app: FastAPI):
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(jokes_router, prefix="/jokes", tags=["Jokes"])
    app.include_router(user_router, prefix="/users", tags=["User Management"])
    app.include_router(chat_router, prefix="/chat", tags=["Chat"])
