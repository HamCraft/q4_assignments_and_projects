from agents.tool import FunctionTool
from context import UserSessionContext

class CheckinSchedulerTool(FunctionTool):
    name = "CheckinSchedulerTool"
    description = "Schedules weekly progress check-ins"

    async def execute(self, input: str, context: UserSessionContext) -> str:
        return "Weekly check-in scheduled for every Monday."