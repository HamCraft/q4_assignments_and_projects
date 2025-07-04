# type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def workout_recommender(
    wrapper: RunContextWrapper[UserSessionContext], 
    fitness_level: str = "beginner",
    focus_area: str = "general"
) -> str:
    """Recommend workout plan based on user's goals and fitness level"""
    
    # Get user's goal from context
    user_goal = wrapper.context.goal
    goal_type = user_goal.get("goal_type", "general_health") if user_goal else "general_health"
    
    # Workout plans based on goal and level
    workouts = {
        "weight_loss": {
            "beginner": {
                "Monday": "20 min walk + 10 min stretching",
                "Tuesday": "Bodyweight: 3x10 squats, 3x5 push-ups, 3x30s plank",
                "Wednesday": "30 min walk or bike ride",
                "Thursday": "Rest or light yoga",
                "Friday": "Bodyweight circuit (repeat Tuesday)",
                "Saturday": "45 min walk + stretching",
                "Sunday": "Rest"
            },
            "intermediate": {
                "Monday": "45 min cardio + 15 min strength",
                "Tuesday": "Full body: squats, push-ups, lunges, planks",
                "Wednesday": "HIIT: 20 min intervals",
                "Thursday": "Upper body strength training",
                "Friday": "Lower body strength training",
                "Saturday": "Long cardio session (60 min)",
                "Sunday": "Active recovery (yoga/walk)"
            }
        },
        "muscle_gain": {
            "beginner": {
                "Monday": "Upper body: push-ups, rows, shoulder press",
                "Tuesday": "Lower body: squats, lunges, calf raises",
                "Wednesday": "Rest or light cardio",
                "Thursday": "Full body circuit",
                "Friday": "Core and flexibility",
                "Saturday": "Compound movements",
                "Sunday": "Rest"
            },
            "intermediate": {
                "Monday": "Chest & Triceps: bench press, dips, flyes",
                "Tuesday": "Back & Biceps: pull-ups, rows, curls",
                "Wednesday": "Legs: squats, deadlifts, lunges",
                "Thursday": "Shoulders & Core: overhead press, planks",
                "Friday": "Arms: focused bicep and tricep work",
                "Saturday": "Full body compound movements",
                "Sunday": "Rest"
            }
        },
        "fitness": {
            "beginner": {
                "Monday": "30 min walk + basic stretching",
                "Tuesday": "Bodyweight exercises (20 min)",
                "Wednesday": "Cardio of choice (30 min)",
                "Thursday": "Strength training (20 min)",
                "Friday": "Flexibility and balance",
                "Saturday": "Outdoor activity (hiking, cycling)",
                "Sunday": "Rest or gentle yoga"
            }
        }
    }
    
    # Get appropriate workout plan
    level = fitness_level.lower()
    if level not in ["beginner", "intermediate"]:
        level = "beginner"
    
    if goal_type in workouts and level in workouts[goal_type]:
        plan = workouts[goal_type][level]
    else:
        plan = workouts["fitness"]["beginner"]
    
    # Update context
    wrapper.context.workout_plan = {
        "goal_type": goal_type,
        "fitness_level": level,
        "plan": plan
    }
    
    result = f"💪 Here's your {level.title()} workout plan for {goal_type.replace('_', ' ').title()}:\n\n"
    for day, exercise in plan.items():
        result += f"**{day}**: {exercise}\n"
    
    result += f"\n⚡ Remember: Start slow and gradually increase intensity. Listen to your body!"
    
    return result