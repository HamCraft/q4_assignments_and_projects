import re
from typing import Optional
from datetime import datetime
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
def analyze_goals(ctx: RunContextWrapper[UserSessionContext], user_input: str) -> dict:
    """
    Parses the user's natural language goals into structured format
    and stores it into the session context under `goal`.
    """

    print("Analyzing user goal...")
    user_input = user_input.lower()
    result = {
        "goal_type": None,
        "target": None,
        "timeframe": None,
        "parsed_at": datetime.utcnow().isoformat()
    }

    # Match weight loss goal
    weight_loss = re.search(r"lose\s+(\d+)\s?(kg|kilograms|pounds?)", user_input)
    if weight_loss:
        amount, unit = weight_loss.groups()
        result["goal_type"] = "weight_loss"
        result["target"] = f"{amount} {unit}"

    # Match muscle gain goal
    elif re.search(r"(gain|build)\s+muscle", user_input):
        result["goal_type"] = "muscle_gain"

    # Match general fitness improvement
    elif re.search(r"(improve|increase|build)\s+(fitness|stamina|endurance)", user_input):
        result["goal_type"] = "improve_fitness"

    # Match timeframe
    time = re.search(r"in\s+(\d+)\s+(days?|weeks?|months?)", user_input)
    if time:
        value, unit = time.groups()
        result["timeframe"] = f"{value} {unit}"

    # Store in session context
    ctx.context.goal = result

    return result
