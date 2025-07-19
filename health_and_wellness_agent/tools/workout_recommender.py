# tools/workout_recommender.py
# Suggests workouts based on user workout preferences and basic fitness principles
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def workout_recommender(wrapper: RunContextWrapper[UserSessionContext]) -> list[str]:
    """
    Recommend a workout routine: warm-up, main set, cooldown.
    """
    prefs = {p.lower() for p in wrapper.context.workout_preferences}
    routine = []
    # Warm-up
    routine.append('5-minute dynamic stretching warm-up')
    # Main exercises
    if 'cardio' in prefs:
        routine.append('20-minute moderate-intensity cardio (jogging or cycling)')
    if 'strength' in prefs or 'strength training' in prefs:
        routine.append('3 sets of bodyweight squats, push-ups, and planks')
    if not prefs:
        routine.append('15-minute HIIT session')
    # Cool-down
    routine.append('5-minute static stretching cooldown')
    return routine