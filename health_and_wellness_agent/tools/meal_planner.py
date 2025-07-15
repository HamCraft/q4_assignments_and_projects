from agents import function_tool, RunContextWrapper
from context import UserSessionContext  
from typing import List
import random


@function_tool
async def suggest_meal_plan(ctx: RunContextWrapper[UserSessionContext]) -> List[str]:
    prefs = ctx.context.dietary_preferences or []
    print("Generating smarter 7 day meal plan...")

    base_meals = {
        "vegetarian": ["Lentil curry", "Veggie stir-fry", "Tofu salad"],
        "high_protein": ["Grilled chicken", "Protein smoothie", "Greek yogurt bowl"],
        "low_carb": ["Zucchini noodles", "Cauliflower rice", "Egg muffins"],
    }

    chosen = []
    for i in range(7):
        meal = []
        for pref in prefs:
            if pref in base_meals:
                meal.append(random.choice(base_meals[pref]))
        chosen.append(f"Day {i+1}: {', '.join(meal) or 'Grilled salmon & veggies'}")
    return chosen
