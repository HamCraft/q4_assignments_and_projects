import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, handoff, set_tracing_disabled, function_tool, RunContextWrapper, GuardrailFunctionOutput, TResponseInputItem, input_guardrail, InputGuardrailTripwireTriggered, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, output_guardrail
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os
from pydantic import BaseModel
# from tools.goal_analyzer import goal_analyzer
# from tools.meal_planner import meal_planner
# from tools.workout_recommender import workout_recommender
# from tools.scheduler import checkin_scheduler_tool


# Load environment variables from .env file / OpenAI Agents SDK Setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_tracing_disabled(disabled=True)

# # # Tool Functions    
# @function_tool
# def get_weather(city: str) -> str:
#     print(f"Getting weather for {city}")
#     return "sunny"

# @function_tool
# def get_temperature(city: str) -> str:
#     print(f"Getting temperature for {city}")
#     return "70 degrees"


async def main():
    # This agent will use the custom LLM provider

    #guardrail 

    class NonHealthDetectionInput(BaseModel):
        is_valid: bool

    class NonHealthDetectionOutput(BaseModel):
        is_valid: bool

    input_guardrail_agent = Agent(
    name="NonHealthInputGuard",
    instructions=(
        "if users says hello, introduce yourself as a health and wellness assistant and said your only for health and wellness related topics. "
        "You are a guardrail agent responsible for determining whether a user's input qualifies as a valid health or wellness request that warrants meaningful action from the assistant. "
        "Return 'true' only if the input meets one or more of the following criteria: "
        "clearly states a health or fitness goal (e.g., weight loss, muscle gain, improved fitness); "
        "requests a meal plan, workout routine, progress tracking, or a scheduled check-in; "
        "seeks guidance or support related to nutrition, exercise, or overall wellness;"
        " gives a positive response to the assistant’s follow-up questions to proceed with planning or coaching. "
        "Return 'false'"
        "if the input is vague, off-topic, or unrelated to health and wellness. "
        "Your purpose is to permit only those inputs that should lead the assistant to analyze goals, trigger appropriate tools, and engage in productive, ongoing conversations."

    ),
    output_type=NonHealthDetectionInput,
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    )

    output_guardrail_agent = Agent(
        name="NonHealthOutputGuard",
        instructions=(
            "You are a guardrail agent that ensures the assistant's response is appropriate ,"
    

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



#Handoff agents    
    EscalationAgent = Agent(
    name="EscalationAgent",
    handoff_description="User wants to speak to a human coach",
    instructions=(
       "You assist users seeking to connect with a human coach or trainer. "
       "Always acknowledge their request with empathy, "
       "provide helpful information, and clearly guide them on how to contact human support or take the next steps."

    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
    
)   
    NutritionExpertAgent = Agent(
    name="Nutrition Expert",
    handoff_description="Complex dietary needs like diabetes or allergies",
    instructions=(
       "You are a specialized nutrition expert focused on complex dietary needs. "
       "Address questions related to diabetes, food allergies, and medical dietary restrictions with care."
       " Provide safe, general nutrition guidance, but always emphasize the importance of consulting a healthcare provider for personalized medical advice."

    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
)
    InjurySupportAgent = Agent(
    name="Injury Support",
    handoff_description="Physical limitations or injury-specific workouts",
    instructions=(
        "You specialize in assisting users with physical limitations or injuries."
        " Offer safe, modified exercise recommendations tailored to common injuries,"
        " always prioritizing safety and low-impact, rehabilitation-friendly movements. "
        "Emphasize the importance of obtaining medical clearance before beginning `any exercise program with an injury."
    ),
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    # output_type=Tutorial
)
    
    def on_escalation_handoff(ctx: RunContextWrapper[None]):
        print("Handing off to escalation agent")

    def on_nutrition_Expert_handoff(ctx: RunContextWrapper[None]):
        print("Handing off to nutrition expert agent")

    def on_injury_support_handoff(ctx: RunContextWrapper[None]):
        print("Handing off to injury support agent")        

    # Main Agent
    agent = Agent(
        name="Health & Wellness Agent",
        instructions="You are a friendly Health & Wellness Assistant. " 
        "Support users by helping them set and analyze fitness goals, " 
        "create personalized meal plans based on dietary preferences, " 
        "recommend appropriate workout routines, track their progress, "
        "and schedule check-ins. Never concatenate tool names or call multiple tools in a single request. " 
        "Ensure each tool call is clearly formatted and handled separately."
,
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        # tools=[goal_analyzer, meal_planner, workout_recommender],
        handoffs=[handoff(EscalationAgent, on_handoff=on_escalation_handoff),
                  handoff(NutritionExpertAgent, on_handoff=on_nutrition_Expert_handoff),
                 handoff(InjurySupportAgent, on_handoff=on_injury_support_handoff)],
        input_guardrails=[input_detection_guardrail],
        output_guardrails=[output_detection_guardrail],
        
    )

    while True:
        user_input = input("Enter your request (or type 'quit' to exit): ").strip()
        if user_input.lower() == "quit":
            print("Exiting. Goodbye!")
            break
        elif user_input == "":
            print("Please enter a request or type 'quit' to exit.")
            continue
        result = Runner.run_streamed(agent, input=user_input)
        try:
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
        except InputGuardrailTripwireTriggered:
            print("❌ Input rejected by guardrail, please try again with a valid input.")
        except OutputGuardrailTripwireTriggered:
            print("⚠️ Output blocked by guardrail, please try again with a valid output.")

    # result = Runner.run_streamed(agent, input="I want to lose 10 pounds in 2 months. Can you help me with a meal plan and workout routine?")
    # try:
    #     async for event in result.stream_events():
    #         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #             print(event.data.delta, end="", flush=True)
    # except InputGuardrailTripwireTriggered:
    #     print("❌ Input rejected by guardrail, please try again with a valid input.")
    # except OutputGuardrailTripwireTriggered:
    #     print("⚠️ Output blocked by guardrail, please try again with a valid output.")  




if __name__ == "__main__":
    asyncio.run(main())