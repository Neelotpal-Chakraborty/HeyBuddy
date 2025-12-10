import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # JWT Configuration
    JWT_SECRET = os.getenv("JWT_SECRET", "secret123")
    # Access token lifetime in minutes (default: 1 day)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    # Refresh token lifetime in days (default: 30 days)
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # OAuth Configuration
    OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "")
    OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # SQLite Database Configuration (no server needed)
    DATABASE_URL = "sqlite:///./heybuddy.db"

settings = Settings()
