import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, handoff, set_tracing_disabled, RunContextWrapper, GuardrailFunctionOutput, TResponseInputItem, input_guardrail, InputGuardrailTripwireTriggered, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, output_guardrail
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from context import UserSessionContext
from custom_agents.escalation_agent import EscalationAgent, on_escalation_handoff
from custom_agents.injury_support_agent import InjurySupportAgent, on_injury_support_handoff
from custom_agents.nutrition_expert_agent import NutritionExpertAgent, on_nutrition_Expert_handoff
from guardrails import input_detection_guardrail, output_detection_guardrail
from tools.goal_analyzer import analyze_goals
from tools.meal_planner import suggest_meal_plan
from tools.workout_recommender import recommend_workouts
from tools.tracker import progress_tracker
from tools.schedule import smart_workout_scheduler


# Load environment variables from .env file / OpenAI Agents SDK Setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_tracing_disabled(disabled=True)

async def main():

    session_context = UserSessionContext(
    name="Ahmed",
    uid=1,
    goal=None,
    diet_preferences=None,
    workout_plan=None,
    meal_plan=None,
    injury_notes=None,
    handoff_logs=[],
    progress_logs=[]
)    

    # Main Agent
    agent = Agent[UserSessionContext](
        name="Health & Wellness Agent",
        instructions="You are a friendly Health & Wellness Assistant. " 
        "Support users by helping them set and analyze fitness goals, " 
        "create personalized meal plans based on dietary preferences, " 
        "recommend appropriate workout routines, track their progress, "
        "and schedule check-ins. Never concatenate tool names or call multiple tools in a single request. " 
        "Ensure each tool call is clearly formatted and handled separately."
,
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        tools=[analyze_goals, suggest_meal_plan, recommend_workouts, progress_tracker, smart_workout_scheduler],
        handoffs=[handoff(EscalationAgent, on_handoff=on_escalation_handoff),
                  handoff(NutritionExpertAgent, on_handoff=on_nutrition_Expert_handoff),
                 handoff(InjurySupportAgent, on_handoff=on_injury_support_handoff)],
        input_guardrails=[input_detection_guardrail],
        output_guardrails=[output_detection_guardrail],
        
    )

    while True:
        user_input = input("Enter your request (or type 'quit' to exit): ").strip()
        if user_input.lower() == "quit":
            print("Exiting. Goodbye!")
            break
        elif user_input == "":
            print("Please enter a request or type 'quit' to exit.")
            continue
        result = Runner.run_streamed(agent, input=user_input, context=session_context)
        try:
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
        except InputGuardrailTripwireTriggered:
            print("❌ Input rejected by guardrail, please try again with a valid input.")
        except OutputGuardrailTripwireTriggered:
            print("⚠️ Output blocked by guardrail, please try again with a valid output.")
  




if __name__ == "__main__":
    asyncio.run(main())