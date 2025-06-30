from agents.tool import FunctionTool
from context import UserSessionContext
from typing import Dict

class ProgressTrackerTool(FunctionTool):
    def __init__(self):
        super().__init__(
            name="ProgressTrackerTool",
            description="Tracks user progress and updates context",
            params_json_schema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Progress update input"}
                },
                "required": ["input"]
            },
            on_invoke_tool=self.execute
        )

    async def execute(self, input: str, context: UserSessionContext) -> Dict[str, str]:
        progress = {"date": "2025-06-30", "update": input}
        context.progress_logs.append(progress)
        return progress