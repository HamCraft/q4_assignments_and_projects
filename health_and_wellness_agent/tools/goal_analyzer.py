# tools/goal_analyzer.py
# Analyzes the user's fitness and dietary goals with simple heuristics
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def goal_analyzer(wrapper: RunContextWrapper[UserSessionContext]) -> dict:
    """
    Categorize user goals into difficulty tiers based on key terms.
    """
    insights = {}
    recommendations = []
    for goal in wrapper.context.goals:
        lower = goal.lower()
        if any(word in lower for word in ['lose weight', 'slim', 'fat']):
            insights[goal] = 'challenging'
            recommendations.append('Set small milestones for weight loss')
        elif any(word in lower for word in ['gain muscle', 'bulk', 'strength']):
            insights[goal] = 'moderate'
            recommendations.append('Incorporate progressive overload in workouts')
        else:
            insights[goal] = 'easy'
            recommendations.append('Maintain consistency to reach your goal')
    return {
        'analyzed_goals': insights,
        'recommendations': recommendations
    }