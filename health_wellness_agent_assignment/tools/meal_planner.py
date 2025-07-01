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
        try:
            valid_diets = ["vegetarian", "vegan", "diabetic", "gluten-free"]
            input_lower = input.lower()
            if any(diet in input_lower for diet in valid_diets):
                context.diet_preferences = input_lower
            diet = context.diet_preferences or "standard"
            meals = [f"Day {i+1}: {diet} meal - Sample dish" for i in range(7)]
            context.meal_plan = meals
            return meals
        except Exception as e:
            return [f"Error in MealPlannerTool: {str(e)}"]