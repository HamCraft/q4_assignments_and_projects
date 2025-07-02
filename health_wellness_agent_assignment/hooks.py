from agents import RunHooks

class CustomRunHooks(RunHooks):
    def on_agent_start(self, agent, input_data):
        print(f"Agent {agent.name} started with input: {input_data}")

    def on_tool_start(self, tool, input_data):
        print(f"Tool {tool.name} started with input: {input_data}")

    def on_handoff(self, from_agent, to_agent, context):
        print(f"Handing off from {from_agent.name} to {to_agent.name}")
        context.handoff_logs.append(f"Handed off to {to_agent.name}")