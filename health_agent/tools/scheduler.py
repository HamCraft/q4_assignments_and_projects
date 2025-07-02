from agents import Agent, OpenAIChatCompletionsModel, Runner

class Scheduler:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def schedule(self, activity):
        agent = Agent(
            name="Scheduler",
            instructions="Schedule activities in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Schedule {activity}")
        return result.final_output