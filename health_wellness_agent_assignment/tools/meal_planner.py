from agents.tool import FunctionTool
from context import UserSessionContext
from typing import List

class MealPlannerTool(FunctionTool):
    def __init__(self):
        super().__init__(
            name="MealPlannerTool",
            description="Generates a 7-day meal plan based on dietary preferences",
            params_json_schema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Dietary preference input"}
                },
                "required": ["input"]
            },
            on_invoke_tool=self.execute
        )

    async def execute(self, input: str, context: UserSessionContext) -> List[str]:
        valid_diets = ["vegetarian", "vegan", "diabetic", "gluten-free"]
        if any(diet in input.lower() for diet in valid_diets):
            context.diet_preferences = input.lower()
        diet = context.diet_preferences or "standard"
        meals = [f"Day {i+1}: {diet} meal - Sample dish" for i in range(7)]
        context.meal_plan = meals
        return meals