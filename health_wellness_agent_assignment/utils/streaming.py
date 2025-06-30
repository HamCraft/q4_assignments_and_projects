# utils/streaming.py
# Placeholder for streaming utilities
# Streaming is handled in main.py, so this is a minimal placeholder

async def stream_response(runner, agent, input, context):
    async for step in runner.stream(starting_agent=agent, input=input, context=context):
        yield step