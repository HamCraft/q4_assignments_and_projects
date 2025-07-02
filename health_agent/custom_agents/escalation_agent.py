from agents import Agent, OpenAIChatCompletionsModel, Runner

class EscalationAgent:
    def __init__(self):
        self.client = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            api_key="your_gemini_api_key",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    async def escalate(self, message):
        agent = Agent(
            name="EscalationAssistant",
            instructions="Provide escalation advice in haikus.",
            model=self.client,
        )
        result = await Runner.run(agent, message)
        return result.final_output