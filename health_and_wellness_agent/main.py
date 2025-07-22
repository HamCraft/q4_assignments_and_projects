import asyncio
from openai import AsyncOpenAI
from agents import Runner, handoff, set_tracing_disabled,  InputGuardrailTripwireTriggered,  OutputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os
from context import user_ctx
from agent import agent as health_and_wellness_agent
from hooks import HealthHooks


# Load environment variables from .env file / OpenAI Agents SDK Setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_tracing_disabled(disabled=True)

async def main():
    # Initialize user context
    
    print("Welcome to Health & Wellness Planner. Type 'exit' to quit.")
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input == "":
            print("Please enter a request or type 'exit' to quit.")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            stream = Runner.run_streamed(health_and_wellness_agent, input=history, context=user_ctx, hooks=HealthHooks())
            async for event in stream.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
            print()  # newline after streamed response
            # Optionally update history with assistant's reply if your Runner supports it
            # history = stream.to_input_list()  # Uncomment if available
        except InputGuardrailTripwireTriggered:
            print("❌ Input rejected by guardrail, please try again with a valid input.")
        except OutputGuardrailTripwireTriggered:
            print("⚠️ Output blocked by guardrail, please try again with a valid output.")

if __name__ == "__main__":
    asyncio.run(main())


    