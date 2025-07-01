from agents import Agent
from context import UserSessionContext

class NutritionExpertAgent(Agent):
    def __init__(self):
        super().__init__(
            name="NutritionExpertAgent",
            instructions="Handle complex dietary needs like diabetes or allergies.",
            model="gemini-2.0-flash"
        )

    async def on_handoff(self, input: str, context: UserSessionContext) -> str:
        try:
            context.handoff_logs.append(f"Handed off to NutritionExpertAgent: {input}")
            return f"Nutrition expert handling: {input}"
        except Exception as e:
            return f"Error in NutritionExpertAgent: {str(e)}"