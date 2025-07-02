from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from agent import main_agent
from hooks import CustomRunHooks

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found")

# Configure OpenAI client with Gemini
set_tracing_disabled(True)
set_default_openai_api("chat_completions")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)

# Initialize context and runner with hooks
user_context = UserSessionContext(name="User", uid=1)
runner = Runner(hooks=CustomRunHooks())

# Main interaction loop
async def main():
    print("Welcome to the Health & Wellness Planner! Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        async for step in runner.stream(main_agent, input=user_input, context=user_context):
            print(step.pretty_output)

if __name__ == "__main__":
    asyncio.run(main())