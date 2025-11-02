from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ActivityBase(BaseModel):
    name: str
    type: str
    start_date: datetime
    moving_time: Optional[int] = None
    elapsed_time: Optional[int] = None
    distance: Optional[float] = None
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    average_power: Optional[float] = None
    max_power: Optional[float] = None
    tss: Optional[float] = None
    intensity_factor: Optional[float] = None
    normalized_power: Optional[float] = None
    description: Optional[str] = None
    tags: Optional[str] = None

class ActivityCreate(ActivityBase):
    intervals_icu_id: str

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None

class Activity(ActivityBase):
    id: int
    intervals_icu_id: str
    created_at: datetime
    updated_at: datetime
    synced_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ActivitySummary(BaseModel):
    total_activities: int
    total_distance: float
    total_moving_time: int
    avg_distance: float
    recent_activity: Optional[Activity] = None
    
class SyncStatus(BaseModel):
    last_sync: Optional[datetime] = None
    activities_synced: int
    status: str = "success"
    message: Optional[str] = None