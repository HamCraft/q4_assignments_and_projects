from agents import Agent, OpenAIChatCompletionsModel, Runner

class InjurySupportAgent:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def support(self, injury):
        agent = Agent(
            name="InjurySupport",
            instructions="Offer injury support in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Support for {injury}")
        return result.final_output