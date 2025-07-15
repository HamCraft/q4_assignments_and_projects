from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from agent import agent as health_and_wellness_agent

app = FastAPI()

# CORS Middleware for allowing frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Be more specific in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    query: str

async def stream_agent_response(query: str):
    """
    This is an async generator that yields response chunks from the agent.
    """
    runner = Runner()
    # Use run_streamed to get an async iterator of events
    result = runner.run_streamed(health_and_wellness_agent, input=query)
    
    try:
        async for event in result.stream_events():
            # Filter for the event that contains the text delta
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                text_chunk = event.data.delta
                yield text_chunk
                # A small sleep can help prevent overwhelming the client
                # and ensures chunks are sent as they arrive.
                await asyncio.sleep(0.01)
    except Exception as e:
        print(f"An error occurred during streaming: {e}")
        yield "An error occurred."


@app.post("/api/chat")
async def chat_with_agent(user_query: UserQuery):
    """
    This endpoint now returns a streaming response.
    """
    # Return a StreamingResponse, passing the async generator function
    return StreamingResponse(
        stream_agent_response(user_query.query),
        media_type="text/plain"
    )


@app.get("/api")
def home():
    return {"status": "Health and Wellness Agent API is running!"}