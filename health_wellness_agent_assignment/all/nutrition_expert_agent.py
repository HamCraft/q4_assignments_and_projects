from agents import Agent

nutrition_expert_agent = Agent(
    name="NutritionExpert",
    instructions="You are a nutrition expert. Help users with complex dietary needs like diabetes or allergies. Provide detailed dietary advice and meal plans tailored to their conditions.",
    model="gemini-2.0-flash"
)