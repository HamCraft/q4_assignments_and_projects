from agents.tool import FunctionTool
from context import UserSessionContext
from typing import Dict

class ProgressTrackerTool(FunctionTool):
    name = "ProgressTrackerTool"
    description = "Tracks user progress and updates context"

    async def execute(self, input: str, context: UserSessionContext) -> Dict[str, str]:
        progress = {"date": "2025-06-30", "update": input}
        context.progress_logs.append(progress)
        return progress