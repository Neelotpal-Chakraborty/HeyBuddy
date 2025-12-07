from datetime import datetime, timedelta
import jwt
from app.core.config import settings

class JWTManager:
    @staticmethod
    def create_access_token(data: dict):
        payload = {
            "sub": data["sub"],
            "email": data["email"],
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    @staticmethod
    def create_refresh_token(data: dict):
        payload = {
            "sub": data["sub"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
