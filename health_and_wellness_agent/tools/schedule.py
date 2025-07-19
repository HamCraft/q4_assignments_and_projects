from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def checkin_scheduler(wrapper: RunContextWrapper[UserSessionContext]) -> dict[str, str]:
    """
    Merge default check-ins with user-defined schedule slots.
    """
    defaults = {'morning': '7:00 AM', 'evening': '7:00 PM'}
    # Override with user schedule where provided
    merged = {**defaults, **wrapper.context.schedule}
    return merged