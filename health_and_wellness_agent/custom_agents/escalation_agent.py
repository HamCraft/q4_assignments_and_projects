from setup import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper
from context import UserSessionContext




EscalationAgent = Agent[UserSessionContext](
    name="EscalationAgent",
    handoff_description="User wants to speak to a human coach",
    instructions=(
       "You assist users by being a human coach or trainer. "
       "Always acknowledge their request with empathy, "
       "provide helpful information"

    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
    
) 

def on_escalation_handoff(ctx: RunContextWrapper[None]):
        print("Handing off to escalation agent")