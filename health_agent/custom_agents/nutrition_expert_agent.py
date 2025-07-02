from agents import Agent, OpenAIChatCompletionsModel, Runner

class NutritionExpertAgent:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def advise(self, query):
        agent = Agent(
            name="NutritionExpert",
            instructions="Give nutrition advice in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, query)
        return result.final_output