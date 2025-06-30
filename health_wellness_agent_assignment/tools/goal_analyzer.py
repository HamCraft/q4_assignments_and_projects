from agents.tool import FunctionTool
from context import UserSessionContext

class GoalAnalyzerTool(FunctionTool):
    def __init__(self):
        super().__init__(
            name="GoalAnalyzerTool",
            description="Analyzes user goals and converts them into structured format",
            params_json_schema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "User goal input"}
                },
                "required": ["input"]
            },
            on_invoke_tool=self.execute
        )

    async def execute(self, input: str, context: UserSessionContext) -> dict:
        try:
            # Simple parsing for demo purposes
            input_lower = input.lower()
            parts = input_lower.split()
            quantity = next((word for word in parts if word.isdigit()), "5")
            metric = "kg" if "kg" in input_lower else "lbs"
            duration = next((parts[i + 1] for i, word in enumerate(parts) if word == "in"), "2 months")
            goal = {"quantity": int(quantity), "metric": metric, "duration": duration}
            context.goal = goal
            return goal
        except Exception as e:
            return {"error": f"Failed to analyze goal: {str(e)}"}