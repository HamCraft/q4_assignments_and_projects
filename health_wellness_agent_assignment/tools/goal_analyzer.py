from agents.tool import FunctionTool
from context import UserSessionContext

class GoalAnalyzerTool(FunctionTool):
    name = "GoalAnalyzerTool"
    description = "Analyzes user goals and converts them into structured format"

    async def execute(self, input: str, context: UserSessionContext) -> dict:
        # Simple parsing for demo purposes
        parts = input.lower().split()
        quantity = next((word for word in parts if word.isdigit()), "5")
        metric = "kg" if "kg" in input.lower() else "lbs"
        duration = next((parts[i + 1] for i, word in enumerate(parts) if word == "in"), "2 months")
        context.goal = {"quantity": int(quantity), "metric": metric, "duration": duration}
        return context.goal