from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, UserRole
from app.schemas import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from fastapi import HTTPException


class UserService:
    """Service for managing user operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            age=user_data.age,
            role=user_data.role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Update user details"""
        user = UserService.get_user_by_id(db, user_id)

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> User:
        """Change user password"""
        user = UserService.get_user_by_id(db, user_id)

        if not verify_password(old_password, user.password):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        user.password = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users_by_role(db: Session, role: UserRole, skip: int = 0, limit: int = 10) -> list[User]:
        """Get users filtered by role"""
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

    @staticmethod
    def user_count(db: Session) -> int:
        """Get total count of users"""
        return db.query(func.count(User.id)).scalar()
