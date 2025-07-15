# from agents import Agent, OpenAIChatCompletionsModel, Runner

# class GoalAnalyzer:
#     def __init__(self):
#         self.client = OpenAIChatCompletionsModel(
#             model="gemini-2.0-flash",
#             api_key="your_gemini_api_key",
#             base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#         )

#     async def analyze(self, goal):
#         agent = Agent(
#             name="GoalAnalyzer",
#             instructions="Analyze health goals in haikus.",
#             model=self.client,
#         )
#         result = await Runner.run(agent, f"Analyze {goal}")
#         return result.final_output