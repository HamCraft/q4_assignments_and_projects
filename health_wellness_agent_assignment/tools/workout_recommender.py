from agents.tool import FunctionTool
from context import UserSessionContext

class WorkoutRecommenderTool(FunctionTool):
    def __init__(self):
        super().__init__(
            name="WorkoutRecommenderTool",
            description="Suggests a weekly workout plan based on user goals",
            params_json_schema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Workout goal input"}
                },
                "required": ["input"]
            },
            on_invoke_tool=self.execute
        )

    async def execute(self, input: str, context: UserSessionContext) -> dict:
        try:
            plan = {"days": ["Monday: Cardio", "Wednesday: Strength", "Friday: Yoga"]}
            context.workout_plan = plan
            return plan
        except Exception as e:
            return {"error": f"Error in WorkoutRecommenderTool: {str(e)}"}