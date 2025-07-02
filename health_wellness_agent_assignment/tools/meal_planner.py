from agents import function_tool
from guardrails import validate_dietary_input, validate_meal_plan_output
import asyncio

@function_tool
async def meal_planner(diet_preferences: str) -> dict:
    """Generates a 7-day meal plan based on dietary preferences.

    Args:
        diet_preferences: The user's dietary preferences (e.g., 'vegetarian', 'vegan').

    Returns:
        A dictionary with a list of meal suggestions for 7 days.
    """
    if not validate_dietary_input(diet_preferences):
        raise ValueError("Invalid dietary preference. Use: 'vegetarian', 'vegan', 'keto', 'gluten-free', or 'diabetic'")
    # Simulate async operation (replace with API call or model-based generation)
    await asyncio.sleep(1)
    meals = [f"{diet_preferences.capitalize()} Meal {i+1}" for i in range(7)]
    return validate_meal_plan_output({"meals": meals}).dict()