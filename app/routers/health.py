from fastapi import APIRouter
from app.services.intervals_client import intervals_client

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Intervals.icu Activity Tracker",
        "version": "1.0.0"
    }

@router.get("/health/intervals")
async def intervals_health_check():
    """Check connection to Intervals.icu API"""
    is_connected = await intervals_client.test_connection()
    
    return {
        "status": "healthy" if is_connected else "unhealthy",
        "service": "Intervals.icu API",
        "connected": is_connected
    }