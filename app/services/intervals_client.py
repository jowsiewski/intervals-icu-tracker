import httpx
import logging
import base64
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class IntervalsICUClient:
    def __init__(self):
        self.base_url = settings.INTERVALS_ICU_BASE_URL
        self.api_key = settings.INTERVALS_ICU_API_KEY
        self.athlete_id = settings.INTERVALS_ICU_ATHLETE_ID
    
    def _get_auth_header(self) -> Dict[str, str]:
        """Create authorization header for Intervals.icu API"""
        if not self.api_key:
            raise ValueError("INTERVALS_ICU_API_KEY not configured")
        
        # Intervals.icu uses Basic Auth with username="API_KEY" and password=api_key
        auth_string = f"API_KEY:{self.api_key}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        return {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test connection to Intervals.icu API"""
        try:
            if not self.api_key or not self.athlete_id:
                logger.warning("Missing API key or athlete ID")
                return False
                
            headers = self._get_auth_header()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/athlete/{self.athlete_id}",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info("Successfully connected to Intervals.icu API")
                    return True
                else:
                    logger.error(f"Failed to connect to Intervals.icu API: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error testing Intervals.icu connection: {e}")
            return False
    
    async def fetch_activities(
        self, 
        oldest: Optional[date] = None, 
        newest: Optional[date] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch activities from Intervals.icu API"""
        try:
            if not self.api_key or not self.athlete_id:
                raise ValueError("Missing API key or athlete ID configuration")
            
            headers = self._get_auth_header()
            
            # Build query parameters
            params = {}
            if oldest:
                params['oldest'] = oldest.isoformat()
            if newest:
                params['newest'] = newest.isoformat()
            if limit:
                params['limit'] = str(limit)
            
            url = f"{self.base_url}/athlete/{self.athlete_id}/activities"
            
            logger.info(f"Fetching activities from Intervals.icu: {url}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    activities = response.json()
                    logger.info(f"Successfully fetched {len(activities)} activities")
                    return activities
                elif response.status_code == 401:
                    logger.error("Unauthorized - check your API key")
                    raise ValueError("Invalid API key or unauthorized access")
                elif response.status_code == 404:
                    logger.error("Athlete not found - check your athlete ID")
                    raise ValueError("Athlete not found")
                else:
                    logger.error(f"API request failed with status {response.status_code}: {response.text}")
                    raise ValueError(f"API request failed: {response.status_code}")
                    
        except httpx.TimeoutException:
            logger.error("Timeout while fetching activities from Intervals.icu")
            raise ValueError("Request timeout")
        except Exception as e:
            logger.error(f"Error fetching activities from Intervals.icu: {e}")
            raise
    
    async def fetch_activity_details(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific activity"""
        try:
            headers = self._get_auth_header()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/activity/{activity_id}",
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to fetch activity {activity_id}: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching activity {activity_id}: {e}")
            return None
    
    def _parse_activity_data(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse activity data from Intervals.icu format to our schema"""
        try:
            # Map Intervals.icu fields to our database schema
            parsed = {
                "intervals_icu_id": str(activity_data.get("id", "")),
                "name": activity_data.get("name", ""),
                "type": activity_data.get("type", ""),
                "start_date": self._parse_datetime(activity_data.get("start_date_local")),
                "moving_time": activity_data.get("moving_time"),
                "elapsed_time": activity_data.get("elapsed_time"), 
                "distance": activity_data.get("distance"),
                "average_speed": activity_data.get("average_speed"),
                "max_speed": activity_data.get("max_speed"),
                "average_heartrate": activity_data.get("average_heartrate"),
                "max_heartrate": activity_data.get("max_heartrate"),
                "average_power": activity_data.get("average_watts"),
                "max_power": activity_data.get("max_watts"),
                "tss": activity_data.get("training_stress_score"),
                "intensity_factor": activity_data.get("intensity_factor"),
                "normalized_power": activity_data.get("normalized_power"),
                "description": activity_data.get("description", ""),
                "tags": ",".join(activity_data.get("tags", [])) if activity_data.get("tags") and isinstance(activity_data.get("tags"), list) else ""
            }
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing activity data: {e}")
            return {}
    
    def _parse_datetime(self, date_string: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from Intervals.icu"""
        if not date_string:
            return None
        
        try:
            # Intervals.icu typically returns ISO format
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            logger.warning(f"Could not parse datetime: {date_string}")
            return None

# Create a global instance
intervals_client = IntervalsICUClient()