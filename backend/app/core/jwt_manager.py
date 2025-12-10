from datetime import datetime, timedelta
import jwt
from app.core.config import settings

class JWTManager:
    @staticmethod
    def create_access_token(data: dict):
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            # Ensure 'sub' is always a string to satisfy JWT libraries that expect a string subject
            "sub": str(data.get("sub") or data.get("user_id")),
            "user_id": data.get("user_id"),
            "email": data.get("email"),
            "exp": expire
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    @staticmethod
    def create_refresh_token(data: dict):
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(data.get("sub") or data.get("user_id")),
            "user_id": data.get("user_id"),
            "exp": expire
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
