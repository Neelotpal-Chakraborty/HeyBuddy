import jwt
from fastapi import HTTPException, Header
from app.core.config import settings

def validate_access_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
