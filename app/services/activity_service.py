from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, date
from typing import List, Optional, Dict, Any
import logging

from app.database import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivitySummary
from app.services.intervals_client import intervals_client

logger = logging.getLogger(__name__)

class ActivityService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_activities(
        self, 
        skip: int = 0, 
        limit: int = 100,
        activity_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Activity]:
        """Get activities with optional filtering"""
        query = self.db.query(Activity)
        
        if activity_type:
            query = query.filter(Activity.type == activity_type)
        
        if start_date:
            query = query.filter(Activity.start_date >= start_date)
        
        if end_date:
            query = query.filter(Activity.start_date <= end_date)
        
        return query.order_by(desc(Activity.start_date)).offset(skip).limit(limit).all()
    
    def get_activity(self, activity_id: int) -> Optional[Activity]:
        """Get a single activity by ID"""
        return self.db.query(Activity).filter(Activity.id == activity_id).first()
    
    def get_activity_by_intervals_id(self, intervals_icu_id: str) -> Optional[Activity]:
        """Get activity by Intervals.icu ID"""
        return self.db.query(Activity).filter(Activity.intervals_icu_id == intervals_icu_id).first()
    
    def create_activity(self, activity_data: ActivityCreate) -> Activity:
        """Create a new activity"""
        db_activity = Activity(**activity_data.dict())
        db_activity.synced_at = datetime.utcnow()
        
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        
        logger.info(f"Created activity: {db_activity.name} (ID: {db_activity.id})")
        return db_activity
    
    def update_activity(self, activity_id: int, activity_data: ActivityUpdate) -> Optional[Activity]:
        """Update an existing activity"""
        db_activity = self.get_activity(activity_id)
        if not db_activity:
            return None
        
        for field, value in activity_data.dict(exclude_unset=True).items():
            setattr(db_activity, field, value)
        
        db_activity.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_activity)
        
        logger.info(f"Updated activity: {db_activity.name} (ID: {db_activity.id})")
        return db_activity
    
    def delete_activity(self, activity_id: int) -> bool:
        """Delete an activity"""
        db_activity = self.get_activity(activity_id)
        if not db_activity:
            return False
        
        self.db.delete(db_activity)
        self.db.commit()
        
        logger.info(f"Deleted activity ID: {activity_id}")
        return True
    
    def get_activity_summary(self) -> ActivitySummary:
        """Get summary statistics for all activities"""
        try:
            total_activities = self.db.query(Activity).count()
            
            # Calculate totals
            totals = self.db.query(
                func.sum(Activity.distance).label("total_distance"),
                func.sum(Activity.moving_time).label("total_moving_time")
            ).first()
            
            total_distance = float(totals.total_distance or 0)
            total_moving_time = int(totals.total_moving_time or 0)
            
            # Get most recent activity
            recent_activity = self.db.query(Activity).order_by(desc(Activity.start_date)).first()
            
            return ActivitySummary(
                total_activities=total_activities,
                total_distance=total_distance,
                total_moving_time=total_moving_time,
                avg_distance=total_distance / total_activities if total_activities > 0 else 0.0,
                recent_activity=recent_activity
            )
        except Exception as e:
            logger.error(f"Error getting activity summary: {e}")
            # Return empty summary on error
            return ActivitySummary(
                total_activities=0,
                total_distance=0.0,
                total_moving_time=0,
                avg_distance=0.0,
                recent_activity=None
            )
    
    async def sync_from_intervals_icu(
        self, 
        oldest: Optional[date] = None,
        newest: Optional[date] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Sync activities from Intervals.icu API"""
        try:
            # Fetch activities from Intervals.icu
            activities_data = await intervals_client.fetch_activities(oldest, newest, limit)
            
            synced_count = 0
            updated_count = 0
            
            for activity_data in activities_data:
                try:
                    # Parse the activity data
                    parsed_data = intervals_client._parse_activity_data(activity_data)
                    
                    if not parsed_data.get("intervals_icu_id"):
                        logger.warning("Skipping activity without ID")
                        continue
                    
                    # Check if activity already exists
                    existing_activity = self.get_activity_by_intervals_id(parsed_data["intervals_icu_id"])
                    
                    if existing_activity:
                        # Update existing activity
                        for field, value in parsed_data.items():
                            if value is not None and field != "intervals_icu_id":
                                setattr(existing_activity, field, value)
                        
                        existing_activity.synced_at = datetime.utcnow()
                        existing_activity.updated_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new activity
                        activity_create = ActivityCreate(**parsed_data)
                        self.create_activity(activity_create)
                        synced_count += 1
                
                except Exception as e:
                    logger.error(f"Error processing activity: {e}")
                    continue
            
            self.db.commit()
            
            return {
                "status": "success",
                "activities_synced": synced_count,
                "activities_updated": updated_count,
                "total_processed": len(activities_data),
                "last_sync": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error syncing activities: {e}")
            return {
                "status": "error",
                "message": str(e),
                "activities_synced": 0,
                "activities_updated": 0
            }