# hooks.py

from agents import RunHooks, RunContextWrapper, Agent

class HealthHooks(RunHooks):
    def __init__(self):
        super().__init__()
        self.event_counter = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    async def on_agent_start(self,
                             context: RunContextWrapper,
                             agent: Agent) -> None:
        self.event_counter += 1
        ui = context.usage.input_tokens or 0
        self.total_input_tokens += ui
        print(f"[Hook] #{self.event_counter} starting {agent.name} (in_tokens={ui})")

    async def on_agent_end(self,
                           context: RunContextWrapper,
                           agent: Agent,
                           output: any) -> None:
        self.event_counter += 1
        ot = context.usage.output_tokens or 0
        self.total_output_tokens += ot
        print(f"[Hook] #{self.event_counter} finished {agent.name} (out_tokens={ot})")

    # This signature MUST accept the tool function itself as the third argument
    async def on_tool_start(self,
                            context: RunContextWrapper,
                            agent: Agent,
                            func_tool) -> None:
        print(f"[Hook] Calling tool: {func_tool.name}")

    # And similarly for after the tool finishes
    async def on_tool_end(self,
                          context: RunContextWrapper,
                          agent: Agent,
                          func_tool,
                          result: any) -> None:
        print(f"[Hook] Tool finished: {func_tool.name} -> {result}")
