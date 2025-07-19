from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class UserSessionContext(BaseModel):
    uid: int
    name: str
    goals: List[str] = Field(default_factory=list)
    dietary_preferences: List[str] = Field(default_factory=list)
    workout_preferences: List[str] = Field(default_factory=list)
    schedule: Dict[str, str] = Field(default_factory=dict)
    progress: Dict[str, float] = Field(default_factory=dict)

user_ctx = UserSessionContext(uid=1, name="Alex")