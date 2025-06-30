from agents.tool import FunctionTool
from context import UserSessionContext
from typing import List

class MealPlannerTool(FunctionTool):
    name = "MealPlannerTool"
    description = "Generates a 7-day meal plan based on dietary preferences"

    async def execute(self, input: str, context: UserSessionContext) -> List[str]:
        diet = context.diet_preferences or "standard"
        meals = [f"Day {i+1}: {diet} meal - Sample dish" for i in range(7)]
        context.meal_plan = meals
        return meals