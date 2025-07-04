# type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
import asyncio

@function_tool
async def meal_planner(
    wrapper: RunContextWrapper[UserSessionContext], 
    dietary_preferences: str = "balanced"
) -> str:
    """Generate a 7-day meal plan based on user preferences"""
    
    # Simulate async processing
    await asyncio.sleep(1)
    
    # Update context
    wrapper.context.diet_preferences = dietary_preferences.lower()
    
    # Simple meal plans based on preferences
    meal_plans = {
        "vegetarian": [
            "Day 1: Oatmeal with fruits, Veggie wrap, Lentil curry with rice",
            "Day 2: Greek yogurt with granola, Quinoa salad, Vegetable stir-fry",
            "Day 3: Smoothie bowl, Caprese sandwich, Chickpea curry",
            "Day 4: Avocado toast, Buddha bowl, Vegetable pasta",
            "Day 5: Chia pudding, Hummus wrap, Black bean tacos",
            "Day 6: Fruit salad, Quinoa soup, Vegetable pizza",
            "Day 7: Pancakes, Greek salad, Mushroom risotto"
        ],
        "keto": [
            "Day 1: Eggs with bacon, Chicken salad, Salmon with broccoli",
            "Day 2: Avocado smoothie, Tuna salad, Beef with asparagus",
            "Day 3: Cheese omelet, Chicken wings, Pork chops with cauliflower",
            "Day 4: Bulletproof coffee, Egg salad, Lamb with green beans",
            "Day 5: Bacon and eggs, Chicken thighs, Steak with spinach",
            "Day 6: Keto pancakes, Sardines, Turkey with Brussels sprouts",
            "Day 7: Cheese platter, Chicken soup, Cod with zucchini"
        ],
        "balanced": [
            "Day 1: Oatmeal with berries, Grilled chicken salad, Salmon with vegetables",
            "Day 2: Greek yogurt, Turkey sandwich, Lean beef with sweet potato",
            "Day 3: Smoothie, Quinoa bowl, Grilled fish with rice",
            "Day 4: Eggs with toast, Chicken wrap, Pasta with vegetables",
            "Day 5: Cereal with milk, Tuna salad, Chicken with broccoli",
            "Day 6: Fruit bowl, Veggie burger, Turkey with quinoa",
            "Day 7: Pancakes, Caesar salad, Grilled chicken with rice"
        ]
    }
    
    # Select appropriate meal plan
    diet_type = dietary_preferences.lower()
    if "vegetarian" in diet_type or "vegan" in diet_type:
        selected_plan = meal_plans["vegetarian"]
        plan_type = "Vegetarian"
    elif "keto" in diet_type or "low carb" in diet_type:
        selected_plan = meal_plans["keto"]
        plan_type = "Keto"
    else:
        selected_plan = meal_plans["balanced"]
        plan_type = "Balanced"
    
    # Update context
    wrapper.context.meal_plan = selected_plan
    
    result = f"🍽️ Here's your 7-day {plan_type} meal plan:\n\n"
    for i, day_plan in enumerate(selected_plan, 1):
        result += f"{day_plan}\n"
    
    result += f"\n💡 This plan is tailored for your {dietary_preferences} preferences!"
    
    return result