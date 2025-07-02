# import asyncio
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool, RunContextWrapper
# from dotenv import load_dotenv
# import os
# from context import UserSessionContext


# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# #Reference: https://ai.google.dev/gemini-api/docs/openai
# client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# set_tracing_disabled(disabled=True)

# @function_tool
# async def goal_analyzer(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     A tool that analyzes the goal of the user.
#     """
#     return f"Analyzing goal: {wrapper.context.goal}"
# @function_tool
# async def meal_planner(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     A tool that helps plan meals for weight loss.
#     """
#     return f"Planning meals based on preferences: {wrapper.context.diet_preferences}"
# @function_tool
# async def schedular(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     A tool that helps schedule workouts and activities.
#     """
#     return f"Scheduling workouts based on the user's preferences and goals: {wrapper.context.workout_plan}"
# @function_tool
# async def progress_tracker(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     A tool that tracks the user's progress towards their weight loss goal.
#     """
#     return f"Tracking progress: {wrapper.context.progress_logs}"
# @function_tool
# async def workout_suggester(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     A tool that suggests workouts based on the user's preferences and goals.
#     """
#     return f"Suggesting workouts based on preferences: {wrapper.context.workout_plan}"
# async def main():
#     escalation_agent = Agent(
#         name="Escalation Agent",
#         instructions="You are an escalation agent that can call other agents.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#     )
#     injury_support_agent = Agent(
#         name="Injury Support Agent",
#         instructions="You are an agent that provides support for injuries.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#     )
#     nutrition_expert_agent = Agent(
#         name="Nutrition Expert Agent",
#         instructions="You are an agent that provides nutrition advice.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#     )
#     agent = Agent[UserSessionContext](
#         name="Assistant",
#         instructions="You are a personal assistant that helps users achieve their weight loss goals. You can call other agents for specialized tasks.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#         tools=[
#             goal_analyzer,
#             meal_planner,
#             schedular,
#             progress_tracker,
#             workout_suggester,
#         ],
#         handoffs=[
#             escalation_agent,
#             injury_support_agent,
#             nutrition_expert_agent,
#         ]
#     )

#     result = await Runner.run(
#         agent,
#         "I want to lose 5kg in 2 months.",
#     )
#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())

# import asyncio
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool, RunContextWrapper
# from dotenv import load_dotenv
# import os
# from context import UserSessionContext
# from pydantic import BaseModel, ConfigDict
# from typing import Optional, List, Dict

# # Load environment variables
# load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Initialize OpenAI client for Gemini API
# client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )
# set_tracing_disabled(disabled=True)

# # Enhanced function tools with connected logic
# @function_tool
# async def goal_analyzer(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     Analyzes the user's goal and updates the context with structured data to guide meal and workout planning.
#     """
#     goal_text = wrapper.context.goal.get("text", "") if wrapper.context.goal else ""
#     if "lose" in goal_text.lower() and "kg" in goal_text.lower():
#         try:
#             weight_loss = float(next(word for word in goal_text.split() if word.replace(".", "").isdigit()))
#             duration = next((word for word in goal_text.split() if "month" in word.lower()), "2 months")
#             wrapper.context.goal = {"type": "weight_loss", "amount_kg": weight_loss, "duration": duration}
#             return f"Goal set: Lose {weight_loss}kg in {duration}. Ready to create meal and workout plans."
#         except:
#             return "Unable to parse weight loss goal. Please clarify (e.g., 'lose 5kg in 2 months')."
#     elif "injury" in goal_text.lower():
#         injury_area = "knee" if "knee" in goal_text.lower() else "unspecified"
#         wrapper.context.injury_notes = f"Injury: {injury_area}. Use low-impact exercises and anti-inflammatory meals."
#         wrapper.context.goal = {"type": "injury_management", "area": injury_area}
#         return f"Goal set: Manage {injury_area} injury. Plans will prioritize recovery."
#     return "Please provide a clear goal (e.g., 'lose 5kg in 2 months' or 'manage knee injury')."

# @function_tool
# async def meal_planner(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     Generates a 7-day meal plan based on the user's goal and dietary preferences.
#     For weight loss, ensures a calorie deficit. For injuries, includes anti-inflammatory foods.
#     """
#     goal = wrapper.context.goal or {}
#     diet_prefs = wrapper.context.diet_preferences or "balanced"
#     if goal.get("type") == "weight_loss":
#         amount_kg = goal.get("amount_kg", 5)
#         duration = goal.get("duration", "2 months")
#         weeks = 8 if "2 months" in duration else 4
#         daily_deficit = (amount_kg * 7700) / (weeks * 7)  # 1kg = ~7700 kcal
#         meal_plan = [
#             f"Day 1: Breakfast: Oatmeal with berries (300 kcal, {diet_prefs}); Lunch: Grilled chicken salad (400 kcal); Dinner: Baked salmon with quinoa (500 kcal); Snack: Greek yogurt (150 kcal)",
#             f"Day 2: Breakfast: Greek yogurt with granola (350 kcal, {diet_prefs}); Lunch: Turkey wrap with veggies (400 kcal); Dinner: Stir-fried tofu with broccoli (450 kcal); Snack: Apple with almond butter (150 kcal)",
#             f"Day 3: Breakfast: Smoothie with spinach, banana (300 kcal, {diet_prefs}); Lunch: Quinoa bowl with avocado (400 kcal); Dinner: Grilled chicken with sweet potato (500 kcal); Snack: Mixed nuts (150 kcal)",
#             f"Day 4: Breakfast: Whole-grain toast with avocado (350 kcal, {diet_prefs}); Lunch: Tuna salad with greens (400 kcal); Dinner: Baked cod with vegetables (450 kcal); Snack: Berries (100 kcal)",
#             f"Day 5: Breakfast: Oatmeal with chia seeds (300 kcal, {diet_prefs}); Lunch: Grilled shrimp salad (400 kcal); Dinner: Turkey meatballs with zucchini noodles (500 kcal); Snack: Carrot sticks with hummus (150 kcal)",
#             f"Day 6: Breakfast: Greek yogurt with fruit (350 kcal, {diet_prefs}); Lunch: Chicken quinoa bowl (400 kcal); Dinner: Baked trout with asparagus (450 kcal); Snack: Almonds (150 kcal)",
#             f"Day 7: Breakfast: Smoothie with kale, berries (300 kcal, {diet_prefs}); Lunch: Veggie wrap with hummus (400 kcal); Dinner: Grilled chicken with roasted veggies (500 kcal); Snack: Orange (100 kcal)",
#             f"Note: Target daily calorie deficit ~{int(daily_deficit)} kcal. Adjust portions as needed."
#         ]
#         wrapper.context.meal_plan = meal_plan
#         return f"7-day meal plan for {amount_kg}kg weight loss:\n" + "\n".join(meal_plan)

#     elif goal.get("type") == "injury_management":
#         injury_area = goal.get("area", "unspecified")
#         meal_plan = [
#             f"Day 1: Breakfast: Turmeric smoothie with berries (anti-inflammatory); Lunch: Quinoa salad with greens; Dinner: Grilled salmon with sweet potato; Snack: Walnuts",
#             f"Day 2: Breakfast: Oatmeal with chia seeds; Lunch: Avocado toast with egg; Dinner: Baked chicken with broccoli; Snack: Blueberries",
#             f"Day 3: Breakfast: Greek yogurt with flaxseeds; Lunch: Tuna salad with spinach; Dinner: Grilled fish with quinoa; Snack: Almonds",
#             f"Day 4: Breakfast: Smoothie with kale, ginger; Lunch: Chickpea salad with olive oil; Dinner: Turkey with roasted vegetables; Snack: Berries",
#             f"Day 5: Breakfast: Oatmeal with turmeric; Lunch: Grilled shrimp with greens; Dinner: Baked cod with asparagus; Snack: Walnuts",
#             f"Day 6: Breakfast: Greek yogurt with berries; Lunch: Quinoa bowl with avocado; Dinner: Chicken with sweet potato; Snack: Mixed nuts",
#             f"Day 7: Breakfast: Smoothie with spinach, flaxseeds; Lunch: Veggie salad with olive oil; Dinner: Salmon with steamed broccoli; Snack: Blueberries",
#             f"Note: Focus on anti-inflammatory foods to support {injury_area} recovery."
#         ]
#         wrapper.context.meal_plan = meal_plan
#         return f"7-day meal plan for {injury_area} injury recovery:\n" + "\n".join(meal_plan)
#     return "No goal specified for meal planning."

# @function_tool
# async def schedular(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     Creates a 7-day workout schedule based on the user's goal and any injuries.
#     """
#     goal = wrapper.context.goal or {}
#     if goal.get("type") == "weight_loss":
#         workout_plan = {
#             "Day 1": "30 min brisk walking, 15 min bodyweight squats",
#             "Day 2": "20 min cycling, 10 min core exercises",
#             "Day 3": "30 min swimming, 15 min stretching",
#             "Day 4": "25 min jogging, 10 min push-ups",
#             "Day 5": "30 min brisk walking, 15 min lunges",
#             "Day 6": "20 min stationary bike, 10 min planks",
#             "Day 7": "Rest or 30 min light yoga",
#             "Note": "Aim for 150-300 min/week moderate activity."
#         }
#         wrapper.context.workout_plan = workout_plan
#         return f"7-day workout schedule for weight loss:\n" + "\n".join([f"{day}: {activity}" for day, activity in workout_plan.items()])
#     elif goal.get("type") == "injury_management":
#         injury_area = goal.get("area", "unspecified")
#         workout_plan = {
#             "Day 1": "15 min gentle yoga (avoid knee strain)",
#             "Day,Jogging is a high-impact exercise that can exacerbate knee injuries. Instead, consider these low-impact alternatives: 2": "20 min upper body resistance bands",
#             "Day 3": "15 min seated stretching",
#             "Day 4": "10 min core exercises (seated)",
#             "Day 5": "15 min light yoga",
#             "Day 6": "20 min arm strength training",
#             "Day 7": "Rest or 10 min stretching",
#             "Note": f"Low-impact exercises to protect {injury_area}."
#         }
#         wrapper.context.workout_plan = workout_plan
#         return f"7-day workout schedule for {injury_area} injury:\n" + "\n".join([f"{day}: {activity}" for day, activity in workout_plan.items()])
#     return "No goal specified for scheduling."

# @function_tool
# async def progress_tracker(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     Logs progress for the user's goal, including weight loss or injury recovery updates.
#     """
#     goal = wrapper.context.goal or {}
#     if goal.get("type") == "weight_loss":
#         progress = {"date": "2025-07-01", "status": f"Started {goal.get('amount_kg')}kg weight loss journey", "weight_lost_kg": 0}
#         wrapper.context.progress_logs.append(progress)
#         return f"Progress tracking started: Log your weight weekly to monitor {goal.get('amount_kg')}kg loss."
#     elif goal.get("type") == "injury_management":
#         progress = {"date": "2025-07-01", "status": f"Started recovery for {goal.get('area')} injury", "notes": "Monitor pain and mobility"}
#         wrapper.context.progress_logs.append(progress)
#         return f"Progress tracking started: Log {goal.get('area')} injury recovery updates weekly."
#     return "No goal specified for tracking."

# @function_tool
# async def workout_suggester(wrapper: RunContextWrapper[UserSessionContext]):
#     """
#     Suggests workouts tailored to the user's goal and any injuries.
#     """
#     goal = wrapper.context.goal or {}
#     if goal.get("type") == "weight_loss":
#         suggestions = [
#             "30 min brisk walking (low impact, burns ~150 kcal)",
#             "15 min bodyweight squats and lunges",
#             "20 min swimming or cycling (cardio)"
#         ]
#         return f"Workout suggestions for weight loss:\n" + "\n".join(suggestions)
#     elif goal.get("type") == "injury_management":
#         injury_area = goal.get("area", "unspecified")
#         suggestions = [
#             f"15 min gentle stretching for {injury_area}",
#             "20 min upper body resistance bands",
#             "10 min seated core exercises"
#         ]
#         return f"Workout suggestions for {injury_area} injury:\n" + "\n".join(suggestions)
#     return "No goal specified for workout suggestions."

# async def main():
#     # Define agents with cohesive instructions
#     escalation_agent = Agent(
#         name="Escalation Agent",
#         instructions="Delegate tasks to specialized agents based on user needs. For injuries, hand off to Injury Support Agent. For detailed nutrition plans, hand off to Nutrition Expert Agent. Use tools for general planning and tracking.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#     )
#     injury_support_agent = Agent(
#         name="Injury Support Agent",
#         instructions="Provide safe recovery plans for injuries, using low-impact workouts and anti-inflammatory meals. Use goal_analyzer, meal_planner, and schedular to create tailored 7-day plans. Recommend consulting a doctor for severe cases.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#         tools=[goal_analyzer, meal_planner, schedular],
#     )
#     nutrition_expert_agent = Agent(
#         name="Nutrition Expert Agent",
#         instructions="Create detailed 7-day meal plans based on user goals and preferences. For weight loss, ensure a calorie deficit. For injuries, focus on anti-inflammatory foods. Use meal_planner to generate plans.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#         tools=[meal_planner],
#     )
#     agent = Agent[UserSessionContext](
#         name="Assistant",
#         instructions="You are a health and wellness assistant helping users achieve goals like weight loss or injury recovery. For weight loss, create a 7-day meal plan with a calorie deficit and a 7-day workout plan with moderate exercise. For injuries, provide low-impact workouts and anti-inflammatory meals. Use goal_analyzer to parse goals, meal_planner and schedular for 7-day plans, progress_tracker to log progress, and workout_suggester for additional ideas. Hand off to Injury Support Agent for injuries or Nutrition Expert Agent for complex nutrition needs. Provide clear, actionable 7-day plans in the response.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#         tools=[
#             goal_analyzer,
#             meal_planner,
#             schedular,
#             progress_tracker,
#             workout_suggester,
#         ],
#         handoffs=[
#             escalation_agent,
#             injury_support_agent,
#             nutrition_expert_agent,
#         ]
#     )

#     # Interactive user input
#     user_input = input("Enter your health goal (e.g., 'lose 5kg in 2 months' or 'manage knee injury'): ")
#     context = UserSessionContext(
#         name="User",
#         uid=1,
#         goal={"text": user_input},
#         diet_preferences="balanced",
#     )
#     result = await Runner.run(
#         agent,
#         user_input,
#         context=context
#     )
    
#     # Format a comprehensive response
#     goal = context.goal or {}
#     response = [result.final_output]
#     if context.meal_plan:
#         response.append("\nYour 7-Day Meal Plan:")
#         response.extend(context.meal_plan)
#     if context.workout_plan:
#         response.append("\nYour 7-Day Workout Plan:")
#         response.extend([f"{day}: {activity}" for day, activity in context.workout_plan.items()])
#     if context.progress_logs:
#         response.append("\nProgress Tracking:")
#         response.append(context.progress_logs[-1]["status"])
#         response.append("Please log your weight or recovery updates weekly to stay on track!")
#     print("\n".join(response))

# if __name__ == "__main__":
#     asyncio.run(main())
