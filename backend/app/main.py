from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import register_routes
from app.db import create_all_tables

app = FastAPI(title="Full Stack Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables on startup
create_all_tables()

register_routes(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}
