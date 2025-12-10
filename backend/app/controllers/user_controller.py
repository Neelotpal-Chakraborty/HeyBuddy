from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.user_service import UserService
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    LoginRequest,
    PasswordChangeRequest,
)
from app.core.jwt_manager import JWTManager
from app.models import UserRole

router = APIRouter()


@router.post("/register", response_model=UserDetailResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = UserService.create_user(db, user_data)
    return user


@router.post("/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user with email and password"""
    user = UserService.authenticate_user(db, credentials.email, credentials.password)
    
    # Create JWT tokens
    access_token = JWTManager.create_access_token({"user_id": user.id, "email": user.email})
    refresh_token = JWTManager.create_refresh_token({"user_id": user.id, "email": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": UserDetailResponse.from_orm(user),
    }


@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = UserService.get_user_by_id(db, user_id)
    return user


@router.get("/users", response_model=list[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all users with pagination"""
    users = UserService.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/role/{role}", response_model=list[UserResponse])
def get_users_by_role(
    role: UserRole,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get users filtered by role"""
    users = UserService.get_users_by_role(db, role, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}", response_model=UserDetailResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update user details"""
    user = UserService.update_user(db, user_id, user_data)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    UserService.delete_user(db, user_id)
    return None


@router.post("/users/{user_id}/change-password", response_model=UserDetailResponse)
def change_password(
    user_id: int,
    password_data: PasswordChangeRequest,
    db: Session = Depends(get_db),
):
    """Change user password"""
    user = UserService.change_password(
        db, user_id, password_data.old_password, password_data.new_password
    )
    return user


@router.get("/stats/total-users")
def get_total_users(db: Session = Depends(get_db)):
    """Get total number of users"""
    count = UserService.user_count(db)
    return {"total_users": count}
