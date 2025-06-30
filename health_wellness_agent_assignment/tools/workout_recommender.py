from agents.tool import FunctionTool
from context import UserSessionContext

class WorkoutRecommenderTool(FunctionTool):
    name = "WorkoutRecommenderTool"
    description = "Suggests a weekly workout plan based on user goals"

    async def execute(self, input: str, context: UserSessionContext) -> dict:
        plan = {"days": ["Monday: Cardio", "Wednesday: Strength", "Friday: Yoga"]}
        context.workout_plan = plan
        return plan