from agents import function_tool
from guardrails import validate_schedule_output

@function_tool
def checkin_scheduler(input_data: dict) -> dict:
    """Schedules recurring weekly progress checks.

    Args:
        input_data: A dictionary with scheduling preferences (currently unused).

    Returns:
        A dictionary with scheduled check-in times.
    """
    # Mock implementation
    checkins = ["Monday 8 AM", "Thursday 8 AM"]
    return validate_schedule_output({"checkins": checkins}).dict()