# Tracks and updates progress metrics over time
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def progress_tracker(wrapper: RunContextWrapper[UserSessionContext], metric: str, value: float = None) -> float:
    """
    If value provided, update context; otherwise, return current.
    """
    if value is not None:
        wrapper.context.progress[metric] = value
    return wrapper.context.progress.get(metric, 0.0)