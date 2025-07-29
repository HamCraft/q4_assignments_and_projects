#type: ignore
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, ItemHelpers, function_tool
from config import client, model
from dotenv import load_dotenv

@function_tool
def email_sections() -> list[str]:
    """
    Returns the standard sections for a professional email: Greeting, Body, and Closing.
    """
    return ["Greeting", "Body", "Closing"]

load_dotenv()

async def main():
    agent = Agent(
        name="EmailDraftAgent",
        instructions=(
            "First call the `email_sections` tool to retrieve the three key email sections, "
            "then draft a concise, professional email addressing the user's request using those sections."
        ),
        tools=[email_sections],
        model=model,
    )

    result = Runner.run_streamed(
        agent,
        input="Write a professional email to my manager requesting a meeting to discuss project updates.",
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        if event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        if event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool invoked")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Drafted Email:\n{ItemHelpers.text_message_output(event.item)}")

    print("=== Run complete ===")

if __name__ == "__main__":
    asyncio.run(main())
