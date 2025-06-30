from agents.tool import FunctionTool
from context import UserSessionContext

class CheckinSchedulerTool(FunctionTool):
    def __init__(self):
        super().__init__(
            name="CheckinSchedulerTool",
            description="Schedules weekly progress check-ins",
            params_json_schema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Scheduling input"}
                },
                "required": ["input"]
            },
            on_invoke_tool=self.execute
        )

    async def execute(self, input: str, context: UserSessionContext) -> str:
        return "Weekly check-in scheduled for every Monday."