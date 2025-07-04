#type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
import re
import json

@function_tool
async def goal_analyzer(
    wrapper: RunContextWrapper[UserSessionContext], 
    goal_text: str
) -> str:
    """
    Analyze user's health goal and extract structured information.
    Returns a JSON string with keys: goal_type, target_amount, target_unit, timeframe, specific_goal.
    """
    text = goal_text.lower()

    # Define keywords for goal types
    weight_loss_keywords = ['lose', 'weight', 'slim', 'diet', 'fat']
    muscle_gain_keywords = ['gain', 'muscle', 'bulk', 'strong', 'build muscle']
    fitness_keywords = ['fit', 'exercise', 'cardio', 'run', 'endurance', 'stamina']
    general_keywords = ['health', 'wellness', 'healthy', 'lifestyle']

    # Detect goal type
    if any(word in text for word in weight_loss_keywords):
        goal_type = "weight_loss"
    elif any(word in text for word in muscle_gain_keywords):
        goal_type = "muscle_gain"
    elif any(word in text for word in fitness_keywords):
        goal_type = "fitness"
    elif any(word in text for word in general_keywords):
        goal_type = "general_health"
    else:
        goal_type = "unspecified"

    # Extract numbers and units (e.g., 5kg, 10 lbs)
    number_unit_pattern = re.compile(r'(\d+\.?\d*)\s*(kg|kilograms|lbs|pounds|lbs|reps|minutes|hours)?')
    matches = number_unit_pattern.findall(text)

    target_amount = None
    target_unit = None
    if matches:
        target_amount = matches[0][0]
        target_unit = matches[0][1] if matches[0][1] else None

    # Extract timeframe (e.g., "in 2 months", "within 3 weeks")
    timeframe_pattern = re.compile(r'(\d+)\s*(day|week|month|year)s?')
    timeframe_match = timeframe_pattern.search(text)
    timeframe = None
    if timeframe_match:
        timeframe = f"{timeframe_match.group(1)} {timeframe_match.group(2)}{'s' if int(timeframe_match.group(1)) > 1 else ''}"

    # Build structured goal dictionary
    structured_goal = {
        "goal_type": goal_type,
        "target_amount": target_amount,
        "target_unit": target_unit,
        "timeframe": timeframe,
        "specific_goal": goal_text.strip()
    }

    # Save to context for downstream use
    wrapper.context.goal = structured_goal

    # Return a user-friendly confirmation with structured data as JSON string
    response = (
        f"✅ Goal analyzed:\n"
        f"- Type: {goal_type.replace('_', ' ').title()}\n"
        f"- Target: {target_amount or 'Not specified'} {target_unit or ''}\n"
        f"- Timeframe: {timeframe or 'Flexible'}\n"
        f"Let's create a personalized plan for you!"
    )

    # Optionally, return JSON string for programmatic use
    # return json.dumps(structured_goal)

    return response