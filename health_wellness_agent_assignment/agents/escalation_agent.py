from agents import Agent
from context import UserSessionContext

class EscalationAgent(Agent):
    name = "EscalationAgent"
    instructions = "Escalate to a human coach when requested."
    model = "gemini-2.0-flash"

    async def on_handoff(self, input: str, context: UserSessionContext):
        context.handoff_logs.append(f"Handed off to EscalationAgent: {input}")
        return "Connecting you to a human coach."