from setup import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper
from context import UserSessionContext


NutritionExpertAgent = Agent[UserSessionContext](
    name="Nutrition Expert",
    handoff_description="Complex dietary needs like diabetes or allergies",
    instructions=(
       "You are a specialized nutrition expert focused on complex dietary needs. "
       "Address questions related to diabetes, food allergies, and medical dietary restrictions with care."
       " Provide safe, general nutrition guidance, but always emphasize the importance of consulting a healthcare provider for personalized medical advice."

    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
)

def on_nutrition_Expert_handoff(ctx: RunContextWrapper[None]):
    print("Handing off to nutrition expert agent")