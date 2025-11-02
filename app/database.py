from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    intervals_icu_id = Column(String, unique=True, index=True)
    
    # Basic activity info
    name = Column(String, index=True)
    type = Column(String, index=True)
    start_date = Column(DateTime, index=True)
    
    # Duration and distance
    moving_time = Column(Integer)  # seconds
    elapsed_time = Column(Integer)  # seconds
    distance = Column(Float)  # meters
    
    # Performance metrics
    average_speed = Column(Float)  # m/s
    max_speed = Column(Float)  # m/s
    average_heartrate = Column(Float)
    max_heartrate = Column(Float)
    average_power = Column(Float)
    max_power = Column(Float)
    
    # Training metrics
    tss = Column(Float)  # Training Stress Score
    intensity_factor = Column(Float)
    normalized_power = Column(Float)
    
    # Additional data
    description = Column(Text)
    tags = Column(String)
    
    # Sync metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    synced_at = Column(DateTime)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)