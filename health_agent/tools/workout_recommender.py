from agents import Agent, OpenAIChatCompletionsModel, Runner

class WorkoutRecommender:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def recommend(self, goal):
        agent = Agent(
            name="WorkoutRecommender",
            instructions="Recommend workouts in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, f"Recommend workout for {goal}")
        return result.final_output