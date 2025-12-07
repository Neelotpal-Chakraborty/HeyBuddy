from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.core.security import validate_access_token

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
