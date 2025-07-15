from agents import function_tool, RunContextWrapper
from context import UserSessionContext

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