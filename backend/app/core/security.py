import jwt
from fastapi import HTTPException, Header
from app.core.config import settings
from bcrypt import hashpw, checkpw, gensalt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def validate_access_token(authorization: str = Header(None)):
    """Validate JWT access token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Strip common prefixes and surrounding quotes that may appear from clients
    token = authorization.replace("Bearer ", "", 1).strip()
    print(token)
    if (token.startswith("'") and token.endswith("'")) or (
        token.startswith('"') and token.endswith('"')
    ):
        token = token[1:-1]

    # Handle Python bytes repr like: b'eyJ...'
    if token.startswith("b'") and token.endswith("'"):
        token = token[2:-1]

    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
