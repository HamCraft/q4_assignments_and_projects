from agents import function_tool, RunContextWrapper
from context import UserSessionContext




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
