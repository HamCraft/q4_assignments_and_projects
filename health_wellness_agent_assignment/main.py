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

# Set up Gemini API client
gemini_api_key = ""  # Replace with your actual Gemini API key
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
    instructions="You are a Health & Wellness Planner Agent. Help users set health goals, create meal and workout plans, and track progress. Use tools to analyze goals, suggest plans, and schedule check-ins. Handoff to specialized agents for complex needs.",
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