from agents import Agent, OpenAIChatCompletionsModel, Runner

class Tracker:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def track(self, metric):
        agent = Agent(
            name="Tracker",
            instructions="Track health metrics in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Track {metric}")
        return result.final_output