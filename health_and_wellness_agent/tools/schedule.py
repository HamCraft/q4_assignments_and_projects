from agents import function_tool
from pydantic import BaseModel, ValidationError
from typing import List, Dict
import datetime

class CheckinScheduleOutput(BaseModel):
    checkin_day: str
    checkin_time: str
    reminder: str

@function_tool
async def checkin_scheduler(user_id: int) -> List[Dict]:
    """
    Schedules weekly progress check-ins for a user.
    """
    # Input guardrail: Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user_id. Must be a positive integer.")

    # Simulate async processing
    import asyncio
    await asyncio.sleep(1)  # Mimic processing delay

    # Generate weekly check-in schedule (default: every Monday at 9 AM)
    checkins = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for i, day in enumerate(days):
        checkin = CheckinScheduleOutput(
            checkin_day=day,
            checkin_time="09:00 AM",
            reminder=f"Progress check-in for user {user_id} on {day}"
        )
        checkins.append(checkin.dict())

    # Output guardrail: Ensure structured JSON output
    try:
        return checkins
    except ValidationError as e:
        raise ValueError(f"Error structuring check-in schedule: {str(e)}")