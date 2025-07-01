import asyncio
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckinSchedulerTool
from tools.tracker import ProgressTrackerTool
from all.nutrition_expert import NutritionExpertAgent
from all.injury_support import InjurySupportAgent
from all.escalation import EscalationAgent
from guardrails import validate_goal_input, validate_dietary_input
from pydantic import BaseModel
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("gemini_api_key")


# Set up Gemini API client # Replace with your actual Gemini API key
set_tracing_disabled(True)
set_default_openai_api("chat_completions")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

# Define main agent
main_agent = Agent(
    name="HealthWellnessAgent",
    instructions="""
        You are a friendly Health & Wellness Assistant. Help users with:
        - Setting and analyzing fitness goals
        - Creating meal plans based on dietary preferences
        - Recommending workout routines
        - Tracking progress and scheduling check-ins
        - Do NOT concatenate tool names or call multiple tools in a single call.
        - Format tool calls clearly and separately.
        When users ask for meal plans, workout routines, or goal analysis, USE THE APPROPRIATE TOOLS IMMEDIATELY to provide helpful content.
        Tools have default parameters, so use them even if the user doesn't specify all details.
        ALWAYS INCLUDE THE COMPLETE TOOL RESULTS IN YOUR RESPONSE - don't just say 'I've created a plan', show the actual plan details.
        Be encouraging and supportive. Provide immediate value first, then ask follow-up questions for improvements.
        If users mention injuries, complex dietary needs, or want human support, use handoffs.
        """,
    model="gemini-2.0-flash",
    tools=[
        GoalAnalyzerTool(),
        MealPlannerTool(),
        WorkoutRecommenderTool(),
        CheckinSchedulerTool(),
        ProgressTrackerTool()
    ],
    handoffs=[
        NutritionExpertAgent(),
        InjurySupportAgent(),
        EscalationAgent()
    ]
)

async def main():
    user_context = UserSessionContext(
        name="User",
        uid=uuid.uuid4().int & (1<<31)-1,  # Generate a 31-bit integer UID
        handoff_logs=[],
        progress_logs=[]
    )
    
    print("Welcome to the Health & Wellness Planner! Type your request or 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
            
        # Apply input guardrails
        if "goal" in user_input.lower():
            if not validate_goal_input(user_input):
                print("Invalid goal format. Please specify quantity, metric, and duration (e.g., 'lose 5kg in 2 months').")
                continue
        if "vegetarian" in user_input.lower() or "diabetic" in user_input.lower():
            if not validate_dietary_input(user_input):
                print("Invalid dietary input. Please specify valid dietary preferences.")
                continue

        # Execute the agent
        try:
            result = await Runner.run(
                starting_agent=main_agent,
                input=user_input,
                context=user_context
            )
            print(result.final_output if result.final_output else "No response generated.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())