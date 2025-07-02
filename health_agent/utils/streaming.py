from agents import Agent, OpenAIChatCompletionsModel, Runner

class Streaming:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def stream(self, topic):
        agent = Agent(
            name="Streamer",
            instructions="Stream health tips in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Stream about {topic}")
        return result.final_output