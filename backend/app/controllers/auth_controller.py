from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.core.security import validate_access_token
from app.db import get_db
from app.services.user_service import UserService
from app.core.jwt_manager import JWTManager
from app.core.config import settings
import jwt
from fastapi import Body

router = APIRouter()


@router.get("/login")
def login_redirect():
    return AuthService.redirect_to_sso()


@router.get("/callback")
def auth_callback(code: str):
    return AuthService.handle_callback(code)


@router.get("/me")
def user_profile(user=Depends(validate_access_token)):
    return user


@router.post("/debug/token/{user_id}")
def create_debug_token(user_id: int, db: Session = Depends(get_db)):
    """DEV only: create an access token for a user id for testing.
    Remove or secure this in production.
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = JWTManager.create_access_token({"user_id": user.id, "email": user.email})
    return {"access_token": token, "expires_in_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES}


@router.post('/verify')
def verify_token(payload: dict = Body(...)):
    """DEV: Verify a provided token string with the server's JWT secret.
    POST body: { "token": "<JWT>" }
    """
    token = payload.get('token')
    if not token:
        raise HTTPException(status_code=400, detail='Missing token in request body')
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        return { 'valid': True, 'payload': decoded }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail='Invalid token signature')
    except Exception as e:
        raise HTTPException(status_code=401, detail=f'Invalid token: {str(e)}')
