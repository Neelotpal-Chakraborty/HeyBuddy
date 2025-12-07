from fastapi import FastAPI
from app.routes import register_routes

app = FastAPI(title="Full Stack Backend")

register_routes(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}
