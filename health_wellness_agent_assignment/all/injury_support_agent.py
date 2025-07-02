from agents import Agent

injury_support_agent = Agent(
    name="InjurySupport",
    instructions="You are an injury support assistant. Provide workout plans tailored for users with physical limitations or injuries, ensuring safety and recovery.",
    model="gemini-2.0-flash"
)