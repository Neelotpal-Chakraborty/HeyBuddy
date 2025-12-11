from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, ForeignKey, Date
from sqlalchemy.sql import func
from app.db import Base
import enum
from datetime import datetime


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class User(Base):
    """User model for storing user details"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, role={self.role})>"


class Diary(Base):
    """Diary entries for users"""
    __tablename__ = "diary_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Diary(id={self.id}, user_id={self.user_id}, date={self.date})>"


class DiaryVector(Base):
    """Store embeddings for diary entries to support RAG queries"""
    __tablename__ = "diary_vectors"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diary_entries.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    embedding = Column(String, nullable=False)  # JSON array stored as text
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<DiaryVector(id={self.id}, diary_id={self.diary_id}, user_id={self.user_id})>"
