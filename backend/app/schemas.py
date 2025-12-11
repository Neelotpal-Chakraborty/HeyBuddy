from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models import UserRole
from datetime import datetime
from datetime import date
from pydantic import Field
from typing import List


class UserBase(BaseModel):
    """Base schema for user data"""
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    role: UserRole = Field(default=UserRole.USER, description="User's role")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=255, description="User's password (min 8 characters)")


class UserUpdate(BaseModel):
    """Schema for updating user details"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response (without password)"""
    pass


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., min_length=8, description="User's password")


class PasswordChangeRequest(BaseModel):
    """Schema for password change request"""
    old_password: str = Field(..., min_length=8, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class DiaryBase(BaseModel):
    """Base schema for diary entries"""
    user_id: int
    date: date


class DiaryCreate(DiaryBase):
    content: str


class DiaryUpdate(BaseModel):
    content: Optional[str] = None


class DiaryResponse(DiaryBase):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DiaryDatesResponse(BaseModel):
    dates: List[date]
