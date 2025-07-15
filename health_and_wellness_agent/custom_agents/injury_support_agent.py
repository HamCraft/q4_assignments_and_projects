from setup import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper
from context import UserSessionContext


InjurySupportAgent = Agent[UserSessionContext](
    name="Injury Support",
    handoff_description="Physical limitations or injury-specific workouts",
    instructions=(
        "You specialize in assisting users with physical limitations or injuries."
        " Offer safe, modified exercise recommendations tailored to common injuries,"
        " always prioritizing safety and low-impact, rehabilitation-friendly movements. "
        "Emphasize the importance of obtaining medical clearance before beginning `any exercise program with an injury."
    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
)

def on_injury_support_handoff(ctx: RunContextWrapper[None]):
        print("Handing off to injury support agent")