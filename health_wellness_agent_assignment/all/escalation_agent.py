from agents import Agent

escalation_agent = Agent(
    name="EscalationAgent",
    instructions="You handle requests to speak with a human coach. Inform the user that a coach will be contacted and log the request.",
    model="gemini-2.0-flash"
)