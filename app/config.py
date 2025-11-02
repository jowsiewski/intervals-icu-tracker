import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./activities.db")
    
    # Intervals.icu API
    INTERVALS_ICU_API_KEY: str = os.getenv("INTERVALS_ICU_API_KEY", "")
    INTERVALS_ICU_ATHLETE_ID: str = os.getenv("INTERVALS_ICU_ATHLETE_ID", "")
    INTERVALS_ICU_BASE_URL: str = os.getenv("INTERVALS_ICU_BASE_URL", "https://intervals.icu/api/v1")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Scheduler
    FETCH_INTERVAL_MINUTES: int = int(os.getenv("FETCH_INTERVAL_MINUTES", "60"))

settings = Settings()