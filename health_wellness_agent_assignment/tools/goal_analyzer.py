from agents import function_tool
from guardrails import validate_goal_input, validate_goal_output

@function_tool
def goal_analyzer(input_data: str) -> dict:
    """Analyzes user's fitness goal and extracts structured information.

    Args:
        input_data: The user's goal statement (e.g., 'lose 5kg in 2 months').

    Returns:
        A dictionary with the structured goal.
    """
    if not validate_goal_input(input_data):
        raise ValueError("Invalid goal format. Use: '[lose/gain] [number] [kg/lbs] in [number] [months/weeks]'")
    parts = input_data.lower().split()
    goal = {
        "action": parts[0],
        "quantity": float(parts[1]),
        "metric": parts[2],
        "duration": " ".join(parts[4:]) if len(parts) > 4 else None
    }
    return validate_goal_output(goal).dict()