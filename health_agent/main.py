
"""
Enhanced Health & Wellness Assistant
A beginner-friendly AI assistant for meal planning and workout scheduling
"""

import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool, RunContextWrapper
from dotenv import load_dotenv
import os
from context import UserSessionContext
from guardrails import validate_user_input, validate_system_output, SafetyChecks
from typing import Optional, List, Dict

# Setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_tracing_disabled(disabled=True)

# Enhanced Tools with Better Error Handling
@function_tool
async def smart_goal_analyzer(wrapper: RunContextWrapper[UserSessionContext]):
    """Analyzes user goals with safety validation"""
    goal_text = wrapper.context.goal.get("text", "") if wrapper.context.goal else ""
    
    # Validate input first
    valid, msg = validate_user_input(goal_text, wrapper.context.diet_preferences)
    if not valid:
        return f"❌ {msg}. Please provide a safe, clear goal."
    
    goal_lower = goal_text.lower()
    
    # Weight Loss Goals
    if "lose" in goal_lower and "kg" in goal_lower:
        try:
            import re
            numbers = re.findall(r'\d+\.?\d*', goal_text)
            weight_loss = float(numbers[0]) if numbers else 5
            
            # Determine duration
            if "week" in goal_lower:
                duration = "4 weeks"
            elif "month" in goal_lower:
                months = next((word for word in goal_text.split() if word.isdigit()), "2")
                duration = f"{months} months"
            else:
                duration = "2 months"
            
            wrapper.context.goal = {
                "type": "weight_loss", 
                "amount_kg": weight_loss, 
                "duration": duration
            }
            return f"✅ Goal Set: Lose {weight_loss}kg in {duration}. Creating your personalized plans!"
            
        except Exception as e:
            return "❌ Please specify clearly (e.g., 'lose 5kg in 2 months')"
    
    # Injury Management Goals
    elif "injury" in goal_lower or "pain" in goal_lower:
        injury_types = {
            "knee": "knee", "back": "back", "shoulder": "shoulder", 
            "ankle": "ankle", "wrist": "wrist"
        }
        
        injury_area = "general"
        for keyword, area in injury_types.items():
            if keyword in goal_lower:
                injury_area = area
                break
        
        wrapper.context.injury_notes = f"Managing {injury_area} injury with safe recovery approach"
        wrapper.context.goal = {"type": "injury_management", "area": injury_area}
        return f"✅ Goal Set: Manage {injury_area} injury. Creating recovery-focused plans!"
    
    # Fitness Goals
    elif any(word in goal_lower for word in ["fit", "strong", "muscle", "tone"]):
        wrapper.context.goal = {"type": "fitness", "focus": "general_fitness"}
        return "✅ Goal Set: General fitness improvement. Creating balanced plans!"
    
    return "❌ Please specify your goal clearly (weight loss, injury recovery, or fitness)"

@function_tool
async def smart_meal_planner(wrapper: RunContextWrapper[UserSessionContext]):
    """Creates personalized 7-day meal plans with calorie management"""
    goal = wrapper.context.goal or {}
    diet_pref = wrapper.context.diet_preferences or "balanced"
    
    # Base meal templates by diet preference
    meal_templates = {
        "balanced": {
            "breakfast": ["Oatmeal with berries", "Greek yogurt with granola", "Whole grain toast with avocado"],
            "lunch": ["Grilled chicken salad", "Turkey wrap with veggies", "Quinoa bowl with vegetables"],
            "dinner": ["Baked salmon with quinoa", "Grilled chicken with sweet potato", "Stir-fried tofu with broccoli"],
            "snack": ["Greek yogurt", "Mixed nuts", "Apple with almond butter"]
        },
        "vegetarian": {
            "breakfast": ["Veggie smoothie bowl", "Avocado toast with tomato", "Chia pudding with fruit"],
            "lunch": ["Chickpea salad wrap", "Veggie quinoa bowl", "Lentil soup with bread"],
            "dinner": ["Stuffed bell peppers", "Vegetable stir-fry with tofu", "Pasta with marinara"],
            "snack": ["Hummus with veggies", "Trail mix", "Fruit smoothie"]
        }
    }
    
    templates = meal_templates.get(diet_pref, meal_templates["balanced"])
    
    # Generate meal plan based on goal
    if goal.get("type") == "weight_loss":
        amount_kg = goal.get("amount_kg", 5)
        duration = goal.get("duration", "2 months")
        
        # Calculate safe calorie deficit
        weeks = 8 if "2 months" in duration else 4
        daily_deficit = min((amount_kg * 7700) / (weeks * 7), 800)  # Cap at 800 kcal
        
        # Check if deficit is safe
        safe, safety_msg = SafetyChecks.check_calorie_deficit(daily_deficit)
        if not safe:
            return f"❌ {safety_msg}. Please adjust your goal."
        
        meal_plan = []
        for day in range(1, 8):
            breakfast = templates["breakfast"][(day-1) % len(templates["breakfast"])]
            lunch = templates["lunch"][(day-1) % len(templates["lunch"])]
            dinner = templates["dinner"][(day-1) % len(templates["dinner"])]
            snack = templates["snack"][(day-1) % len(templates["snack"])]
            
            daily_calories = 1400 - int(daily_deficit/2)  # Adjust for deficit
            meal_plan.append(
                f"Day {day}: 🥣 {breakfast} (300 kcal) | 🥗 {lunch} (400 kcal) | "
                f"🍽️ {dinner} (500 kcal) | 🍎 {snack} (150 kcal) | Total: ~{daily_calories} kcal"
            )
        
        meal_plan.append(f"💡 Daily deficit: ~{int(daily_deficit)} kcal for healthy {amount_kg}kg loss")
        
    elif goal.get("type") == "injury_management":
        # Anti-inflammatory focused meals
        anti_inflammatory_foods = [
            "Turmeric smoothie with berries", "Salmon with leafy greens", "Walnuts and blueberries",
            "Green tea with ginger", "Sweet potato with olive oil", "Tuna with avocado"
        ]
        
        meal_plan = []
        for day in range(1, 8):
            meal_plan.append(
                f"Day {day}: Focus on anti-inflammatory foods | "
                f"🥣 {anti_inflammatory_foods[day % 3]} | 🥗 Leafy green salad | "
                f"🐟 Omega-3 rich fish | 🥜 Nuts and seeds"
            )
        meal_plan.append("💡 Rich in omega-3, antioxidants, and anti-inflammatory compounds")
    
    else:
        # General fitness meal plan
        meal_plan = []
        for day in range(1, 8):
            breakfast = templates["breakfast"][(day-1) % len(templates["breakfast"])]
            lunch = templates["lunch"][(day-1) % len(templates["lunch"])]
            dinner = templates["dinner"][(day-1) % len(templates["dinner"])]
            meal_plan.append(f"Day {day}: 🥣 {breakfast} | 🥗 {lunch} | 🍽️ {dinner}")
        meal_plan.append("💡 Balanced nutrition for general fitness")
    
    # Validate output
    valid, validation_msg = validate_system_output(meal_plan, {f"Day {i}": "placeholder" for i in range(1, 8)})
    if not valid:
        return f"❌ Meal plan validation failed: {validation_msg}"
    
    wrapper.context.meal_plan = meal_plan
    return f"✅ 7-Day Meal Plan Created ({diet_pref} diet):\n" + "\n".join(meal_plan)

@function_tool
async def smart_workout_scheduler(wrapper: RunContextWrapper[UserSessionContext]):
    """Creates safe, personalized workout schedules"""
    goal = wrapper.context.goal or {}
    
    if goal.get("type") == "weight_loss":
        # Progressive cardio + strength for weight loss
        workout_plan = {
            "Day 1": "🚶‍♀️ 30min brisk walk + 10min bodyweight squats",
            "Day 2": "🚴‍♀️ 25min cycling + 10min core exercises", 
            "Day 3": "🏊‍♀️ 30min swimming OR 🚶‍♀️ 45min walk",
            "Day 4": "💪 20min strength training + 15min stretching",
            "Day 5": "🚶‍♀️ 35min brisk walk + 10min lunges",
            "Day 6": "🚴‍♀️ 30min low-intensity cardio + yoga",
            "Day 7": "🧘‍♀️ Active recovery: 30min gentle yoga or rest",
            "Note": "Burn 300-500 calories per session for weight loss"
        }
        
    elif goal.get("type") == "injury_management":
        injury_area = goal.get("area", "general")
        # Ultra-safe, low-impact recovery workouts
        workout_plan = {
            "Day 1": "🧘‍♀️ 15min gentle stretching (avoid strain)",
            "Day 2": "💪 10min seated upper body exercises",
            "Day 3": "🏊‍♀️ 15min water therapy OR gentle walking",
            "Day 4": "🧘‍♀️ 10min meditation + breathing exercises", 
            "Day 5": "💪 15min resistance band exercises (light)",
            "Day 6": "🚶‍♀️ 10min slow walk + 10min stretching",
            "Day 7": "😴 Complete rest day",
            "Note": f"Recovery-focused for {injury_area} injury - listen to your body!"
        }
        
    else:
        # General fitness routine
        workout_plan = {
            "Day 1": "💪 30min full-body strength training",
            "Day 2": "🏃‍♀️ 25min cardio + 10min core",
            "Day 3": "🧘‍♀️ 30min yoga or flexibility",
            "Day 4": "💪 25min upper body + 15min cardio",
            "Day 5": "🦵 25min lower body + 10min stretching", 
            "Day 6": "🏃‍♀️ 30min cardio of choice",
            "Day 7": "🧘‍♀️ Active recovery or rest",
            "Note": "Balanced fitness for overall health"
        }
    
    # Validate workout plan
    valid, validation_msg = validate_system_output([], workout_plan)
    if not valid:
        return f"❌ Workout plan validation failed: {validation_msg}"
    
    wrapper.context.workout_plan = workout_plan
    schedule_text = "\n".join([f"{day}: {activity}" for day, activity in workout_plan.items()])
    return f"✅ 7-Day Workout Schedule Created:\n{schedule_text}"

@function_tool
async def progress_tracker(wrapper: RunContextWrapper[UserSessionContext]):
    """Simple progress tracking setup"""
    goal = wrapper.context.goal or {}
    
    if goal.get("type") == "weight_loss":
        tracker_msg = f"📊 Weight Loss Tracker Started!\n" \
                     f"🎯 Goal: {goal.get('amount_kg')}kg in {goal.get('duration')}\n" \
                     f"📅 Weigh yourself weekly, same day/time\n" \
                     f"📝 Log: weight, energy level, how you feel"
        
    elif goal.get("type") == "injury_management":
        tracker_msg = f"📊 Recovery Tracker Started!\n" \
                     f"🎯 Goal: {goal.get('area')} injury recovery\n" \
                     f"📅 Daily check: pain level (1-10), mobility, mood\n" \
                     f"📝 Note improvements and setbacks"
    else:
        tracker_msg = "📊 Fitness Tracker Started!\n" \
                     "📅 Weekly check: strength, endurance, flexibility\n" \
                     "📝 Log workouts completed and how you feel"
    
    wrapper.context.progress_logs = [{"status": "tracking_started", "date": "2025-07-02"}]
    return tracker_msg

# Simple Agent Setup
async def create_health_assistant():
    """Creates the main health assistant agent"""
    return Agent[UserSessionContext](
        name="Health & Wellness Assistant",
        instructions="""You are a friendly, beginner-friendly health assistant. 
        
        🎯 Your job: Help users achieve health goals safely
        📋 Always use: goal analyzer → meal planner → workout scheduler → progress tracker
        ⚠️  Safety first: Never recommend extreme diets or dangerous exercises
        💬 Be encouraging and explain things simply
        
        For each user:
        1. Understand their goal clearly
        2. Create personalized 7-day meal plan  
        3. Design safe 7-day workout schedule
        4. Set up progress tracking
        5. Add medical disclaimer
        
        Keep responses organized with emojis and clear sections.""",
        
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        tools=[smart_goal_analyzer, smart_meal_planner, smart_workout_scheduler, progress_tracker]
    )

async def main():
    """Main application function"""
    print("🌟 Welcome to Your Personal Health & Wellness Assistant! 🌟")
    print("=" * 60)
    
    # Get user input with validation
    while True:
        print("\n💬 What's your health goal?")
        print("Examples:")
        print("• 'lose 5kg in 2 months'")
        print("• 'manage knee injury'") 
        print("• 'get fit and strong'")
        
        user_input = input("\n👉 Your goal: ").strip()
        
        if not user_input:
            print("❌ Please enter a goal!")
            continue
            
        # Quick validation
        valid, msg = validate_user_input(user_input)
        if not valid:
            print(f"❌ {msg}")
            continue
        else:
            break
    
    # Get diet preference
    print("\n🍽️  Diet preference? (balanced/vegetarian/vegan/keto)")
    diet_pref = input("👉 Diet (or press Enter for 'balanced'): ").strip().lower() or "balanced"
    
    print(f"\n🔄 Creating your personalized plan...")
    print("=" * 40)
    
    try:
        # Create assistant and context
        assistant = await create_health_assistant()
        context = UserSessionContext(
            name="User",
            uid=1,
            goal={"text": user_input},
            diet_preferences=diet_pref,
        )
        
        # Run the assistant
        result = await Runner.run(assistant, user_input, context=context)
        
        # Display results with better formatting
        print("\n🎉 YOUR PERSONALIZED HEALTH PLAN")
        print("=" * 50)
        print(result.final_output)
        
        # Add medical disclaimer
        print(f"\n{SafetyChecks.medical_disclaimer()}")
        
        print("\n✨ Tips for Success:")
        print("• Start slowly and listen to your body")
        print("• Stay hydrated and get enough sleep") 
        print("• Track your progress weekly")
        print("• Consult a doctor if you have concerns")
        
        print(f"\n🚀 You've got this! Start your journey today!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please try again or consult the documentation.")

if __name__ == "__main__":
    asyncio.run(main())