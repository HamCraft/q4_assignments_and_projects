# Main Agent
from agents import Agent, OpenAIChatCompletionsModel
from setup import client
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.workout_recommender import workout_recommender
from tools.tracker import progress_tracker
from tools.schedule import checkin_scheduler
from guardrails import input_detection_guardrail, output_detection_guardrail
from custom_agents.escalation_agent import EscalationAgent, on_escalation_handoff
from custom_agents.injury_support_agent import InjurySupportAgent, on_injury_support_handoff
from custom_agents.nutrition_expert_agent import NutritionExpertAgent, on_nutrition_Expert_handoff
from agents import Runner, handoff
from context import UserSessionContext


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
        tools=[goal_analyzer, meal_planner, workout_recommender, progress_tracker, checkin_scheduler],
        handoffs=[handoff(EscalationAgent, on_handoff=on_escalation_handoff),
                  handoff(NutritionExpertAgent, on_handoff=on_nutrition_Expert_handoff),
                 handoff(InjurySupportAgent, on_handoff=on_injury_support_handoff)],
        # input_guardrails=[input_detection_guardrail],
        # output_guardrails=[output_detection_guardrail],
        
    )