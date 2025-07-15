from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from typing import List

@function_tool
def recommend_workouts(ctx: RunContextWrapper[UserSessionContext]) -> List[str]:
    print("Customizing workouts...")
    experience = ctx.context.workout_experience or "beginner"
    goals = ctx.context.goals

    plan = []
    for i in range(7):
        if "weight_loss" in goals:
            plan.append(f"Day {i+1}: {experience.title()} Cardio (30 mins) + Core (15 mins)")
        elif "muscle_gain" in goals:
            plan.append(f"Day {i+1}: {experience.title()} Strength Training - Push/Pull/Legs split")
        else:
            plan.append(f"Day {i+1}: {experience.title()} Full-body mixed routine")
    return plan
