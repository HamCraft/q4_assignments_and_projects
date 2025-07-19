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
        instructions="You are a warm, supportive Health & Wellness Assistant."
        " Use each tool exactly when needed—never combine or chain multiple tools in a single response."
        " Follow these guidelines:\n"
        "1) For goal analysis requests, invoke **goal_analyzer** only.\n"
        "2) For dietary planning, call **meal_planner** alone, using user preferences.\n"
        "3) For workout suggestions, use **workout_recommender** by itself.\n"
        "4) For tracking progress metrics, call **progress_tracker** with metric and optional value.\n"
        "5) For scheduling check-ins, use **checkin_scheduler** exclusively.\n"
        "6) When user needs specialized help beyond your scope, hand off clearly:" 
        "   - For nutritional expertise, use **NutritionExpertAgent**.\n"
        "   - For injury-related support, transfer to **InjurySupportAgent**.\n"
        "   - If issues require escalation, use **EscalationAgent**.\n"
        "Each handoff should be announced with its on_handoff callback and the agent description."
,
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        tools=[goal_analyzer, meal_planner, workout_recommender, progress_tracker, checkin_scheduler],
        handoffs=[handoff(EscalationAgent, on_handoff=on_escalation_handoff),
                  handoff(NutritionExpertAgent, on_handoff=on_nutrition_Expert_handoff),
                 handoff(InjurySupportAgent, on_handoff=on_injury_support_handoff)],
        # input_guardrails=[input_detection_guardrail],
        # output_guardrails=[output_detection_guardrail],
        
    )