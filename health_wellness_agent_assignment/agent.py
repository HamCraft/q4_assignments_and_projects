from agents import Agent
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.workout_recommender import workout_recommender
from tools.scheduler import checkin_scheduler
from tools.tracker import progress_tracker
from all.nutrition_expert_agent import nutrition_expert_agent
from all.injury_support_agent import injury_support_agent
from all.escalation_agent import escalation_agent
from context import UserSessionContext

main_agent = Agent(
    name="HealthWellnessPlanner",
    instructions="""You are a health and wellness planner assistant. Help users achieve their fitness and dietary goals by providing personalized plans and tracking progress. Use tools to analyze goals, generate plans, and schedule check-ins.

Steps:
1. If the user provides a goal (e.g., 'lose 5kg in 2 months'), use the goal_analyzer tool and store the result in context.goal.
2. If the user specifies dietary preferences (e.g., 'I'm vegetarian'), use the meal_planner tool and store the result in context.meal_plan.
3. If a goal is set, use the workout_recommender tool to generate a workout plan and store it in context.workout_plan.
4. Use the checkin_scheduler tool to schedule weekly check-ins and store in context.
5. Use the progress_tracker tool to log progress updates in context.progress_logs.
6. Handoff to specialized agents based on user input:
   - For complex dietary needs like 'diabetes' or 'allergies', hand off to NutritionExpert.
   - For physical limitations or injuries like 'knee pain', hand off to InjurySupport.
   - For requests to speak with a human coach, hand off to EscalationAgent.""",
    model="gemini-2.0-flash",
    tools=[
        goal_analyzer,
        meal_planner,
        workout_recommender,
        checkin_scheduler,
        progress_tracker
    ],
    handoffs=[
        nutrition_expert_agent,
        injury_support_agent,
        escalation_agent
    ]
)