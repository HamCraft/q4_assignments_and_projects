from agents import Agent
from context import UserSessionContext

class NutritionExpertAgent(Agent):
    name = "NutritionExpertAgent"
    instructions = "Handle complex dietary needs like diabetes or allergies."
    model = "gemini-2.0-flash"

    async def on_handoff(self, input: str, context: UserSessionContext):
        context.handoff_logs.append(f"Handed off to NutritionExpertAgent: {input}")
        return f"Nutrition expert handling: {input}"