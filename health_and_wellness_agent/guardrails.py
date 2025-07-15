from agents import Agent, GuardrailFunctionOutput, OpenAIChatCompletionsModel, RunContextWrapper, Runner, TResponseInputItem, input_guardrail, output_guardrail
from pydantic import BaseModel
from setup import client



class NonHealthDetectionInput(BaseModel):
        is_valid: bool

class NonHealthDetectionOutput(BaseModel):
        is_valid: bool

input_guardrail_agent = Agent(
name="NonHealthInputGuard",
instructions=(
        "if users says greets, introduce yourself as a health and wellness assistant and said your only for health and wellness related topics. "
        "You are a guardrail agent responsible for determining whether a user's input qualifies as a valid health or wellness request that warrants meaningful action from the assistant. "
        "Return 'true' only if the input meets one or more of the following criteria: "
        "clearly states a health or fitness goal (e.g., weight loss, muscle gain, improved fitness); "
        "requests a meal plan, workout routine, progress tracking, or a scheduled check-in; "
        "seeks guidance or support related to nutrition, exercise, or overall wellness;"
        " gives a positive response to the assistant’s follow-up questions to proceed with planning or coaching. "
        "Return 'false'"
        "if the input is unrelated to health and wellness. "
        "Your purpose is to permit only those inputs that should lead the assistant to analyze goals, trigger appropriate tools, and engage in productive, ongoing conversations."
        "if user wants to exit, let him end the conversation. "
        

    ),
    output_type=NonHealthDetectionInput,
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    )

output_guardrail_agent = Agent(
    name="NonHealthOutputGuard",
        instructions=(
            "You are a guardrail agent that ensures the assistant's response is appropriate ," \
            "relevant, and actionable within the context of goal analyze, meal plan, workout recommend, schedule_check_in , update progress,  health and wellness, . "
            "if user wants to exit, let him end the conversation. "

        ),
        output_type=NonHealthDetectionOutput,
        model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    )

@input_guardrail
async def input_detection_guardrail(
            ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
        
        detection_result = await Runner.run(input_guardrail_agent, input)

        return GuardrailFunctionOutput(
            tripwire_triggered=not detection_result.final_output.is_valid,
            output_info=detection_result.final_output
        )

@output_guardrail
async def output_detection_guardrail(
            ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
        
        detection_result = await Runner.run(output_guardrail_agent, input)

        return GuardrailFunctionOutput(
            tripwire_triggered= not detection_result.final_output.is_valid,
            output_info=detection_result.final_output
        )