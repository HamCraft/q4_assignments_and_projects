from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def meal_planner(wrapper: RunContextWrapper[UserSessionContext]) -> list[dict]:
    """
    Create a 3-meal plan: breakfast, lunch, dinner, adapting to preferences.
    """
    prefs = {p.lower() for p in wrapper.context.dietary_preferences}
    # Sample meal database
    meals = {
        'vegetarian': ['Veggie omelette', 'Quinoa salad', 'Stir-fried tofu with veggies'],
        'vegan': ['Smoothie bowl', 'Lentil soup', 'Chickpea curry with rice'],
        'keto': ['Egg and avocado plate', 'Grilled salmon with greens', 'Zucchini noodles with pesto'],
        'default': ['Oatmeal with fruits', 'Grilled chicken salad', 'Steamed vegetables with rice']
    }

    # Choose meal set based on first matching preference
    for key in meals:
        if key in prefs:
            selected = meals[key]
            break
    else:
        selected = meals['default']

    plan = [
        {'meal': 'Breakfast', 'menu': selected[0]},
        {'meal': 'Lunch', 'menu': selected[1]},
        {'meal': 'Dinner', 'menu': selected[2]}
    ]
    return plan