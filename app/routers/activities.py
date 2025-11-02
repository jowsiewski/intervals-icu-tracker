from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.schemas.activity import Activity, ActivityUpdate, ActivitySummary, SyncStatus
from app.services.activity_service import ActivityService

router = APIRouter()

@router.get("/activities", response_model=List[Activity])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activity_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of activities with optional filtering"""
    activity_service = ActivityService(db)
    activities = activity_service.get_activities(
        skip=skip, 
        limit=limit,
        activity_type=activity_type,
        start_date=start_date,
        end_date=end_date
    )
    return activities

@router.get("/activities/summary", response_model=ActivitySummary)
async def get_activity_summary(db: Session = Depends(get_db)):
    """Get summary statistics for all activities"""
    activity_service = ActivityService(db)
    return activity_service.get_activity_summary()

@router.get("/activities/{activity_id}", response_model=Activity)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a specific activity by ID"""
    activity_service = ActivityService(db)
    activity = activity_service.get_activity(activity_id)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity

@router.put("/activities/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: int, 
    activity_data: ActivityUpdate, 
    db: Session = Depends(get_db)
):
    """Update an activity"""
    activity_service = ActivityService(db)
    activity = activity_service.update_activity(activity_id, activity_data)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity

@router.delete("/activities/{activity_id}")
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Delete an activity"""
    activity_service = ActivityService(db)
    success = activity_service.delete_activity(activity_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"message": "Activity deleted successfully"}

@router.post("/activities/sync", response_model=SyncStatus)
async def sync_activities(
    oldest: Optional[date] = Query(None, description="Oldest date to sync (YYYY-MM-DD)"),
    newest: Optional[date] = Query(None, description="Newest date to sync (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of activities to sync"),
    db: Session = Depends(get_db)
):
    """Manually trigger sync of activities from Intervals.icu"""
    activity_service = ActivityService(db)
    
    # If no oldest date provided, default to 30 days ago
    if oldest is None:
        from datetime import timedelta
        oldest = date.today() - timedelta(days=30)
    
    result = await activity_service.sync_from_intervals_icu(oldest, newest, limit)
    
    return SyncStatus(
        last_sync=result.get("last_sync"),
        activities_synced=result.get("activities_synced", 0),
        status=result.get("status", "error"),
        message=result.get("message")
    )