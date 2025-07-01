from agents import Agent
from context import UserSessionContext

class EscalationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="EscalationAgent",
            instructions="Escalate to a human coach when requested.",
            model="gemini-2.0-flash"
        )

    async def on_handoff(self, input: str, context: UserSessionContext) -> str:
        try:
            context.handoff_logs.append(f"Handed off to EscalationAgent: {input}")
            return "Connecting you to a human coach."
        except Exception as e:
            return f"Error in EscalationAgent: {str(e)}"