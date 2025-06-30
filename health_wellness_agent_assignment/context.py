from pydantic import BaseModel
from typing import List, Dict, Optional

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    injury_notes: Optional[str] = None
    progress_logs: List[Dict[str, str]] = []
    handoff_logs: List[str] = []