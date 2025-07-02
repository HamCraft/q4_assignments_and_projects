from agents import Agent, OpenAIChatCompletionsModel, Runner

class MealPlanner:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def plan(self, diet):
        agent = Agent(
            name="MealPlanner",
            instructions="Plan meals in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Plan meals for {diet}")
        return result.final_output