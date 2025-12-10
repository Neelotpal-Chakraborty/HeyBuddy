from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create database engine with SQLite
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # SQLite specific: allows multiple threads
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
