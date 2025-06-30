from agents import Agent
from context import UserSessionContext

class InjurySupportAgent(Agent):
    def __init__(self):
        super().__init__(
            name="InjurySupportAgent",
            instructions="Provide workout suggestions for users with injuries.",
            model="gemini-2.0-flash"
        )

    async def on_handoff(self, input: str, context: UserSessionContext):
        context.handoff_logs.append(f"Handed off to InjurySupportAgent: {input}")
        context.injury_notes = input
        return f"Injury support handling: {input}"