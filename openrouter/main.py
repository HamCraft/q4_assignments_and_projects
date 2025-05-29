#type: ignore
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os


load_dotenv()

set_tracing_disabled(disabled=True)


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


async def main():
    agent = Agent(
        name="deepseek",
        instructions="You only respond in english.",
        model=OpenAIChatCompletionsModel(model="deepseek/deepseek-chat-v3-0324:free", openai_client=client),
    )
    print("Agent created, Type 'exit' to quit.\n")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        result = await Runner.run(
            agent,
            user_input,
        )
        print(f"Agent: {result.final_output}\n")

asyncio.run(main())