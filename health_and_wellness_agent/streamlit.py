import streamlit as st
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, handoff, set_tracing_disabled, RunContextWrapper, GuardrailFunctionOutput, TResponseInputItem, input_guardrail, InputGuardrailTripwireTriggered, output_guardrail, OutputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from context import UserSessionContext
from tools.goal_analyzer import analyze_goals
from tools.meal_planner import suggest_meal_plan
from tools.workout_recommender import recommend_workouts
from tools.tracker import progress_tracker
from tools.schedule import smart_workout_scheduler

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_tracing_disabled(disabled=True)

# Initialize session state
if 'context' not in st.session_state:
    st.session_state.context = UserSessionContext(
        name="Ahmed",
        uid=1,
        goal=None,
        diet_preferences=None,
        workout_plan=None,
        meal_plan=None,
        injury_notes=None,
        handoff_logs=[],
        progress_logs=[]
    )
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Guardrail models
class NonHealthDetectionInput(BaseModel):
    is_valid: bool

class NonHealthDetectionOutput(BaseModel):
    is_valid: bool

# Input guardrail agent
input_guardrail_agent = Agent(
    name="NonHealthInputGuard",
    instructions=(
        "If user greets, introduce yourself as a health and wellness assistant and state you're only for health and wellness topics. "
        "You are a guardrail agent responsible for determining whether a user's input qualifies as a valid health or wellness request. "
        "Return 'true' only if the input meets one or more of the following criteria: "
        "clearly states a health or fitness goal (e.g., weight loss, muscle gain, improved fitness); "
        "requests a meal plan, workout routine, progress tracking, or a scheduled check-in; "
        "seeks guidance or support related to nutrition, exercise, or overall wellness; "
        "gives a positive response to the assistant’s follow-up questions to proceed with planning or coaching. "
        "Return 'false' if the input is unrelated to health and wellness. "
        "Your purpose is to permit only those inputs that should lead the assistant to analyze goals, trigger tools, and engage in productive conversations. "
        "If user wants to exit, let them end the conversation."
    ),
    output_type=NonHealthDetectionInput,
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
)

# Output guardrail agent
output_guardrail_agent = Agent(
    name="NonHealthOutputGuard",
    instructions=(
        "You are a guardrail agent that ensures the assistant's response is appropriate, "
        "relevant, and actionable within the context of goal analysis, meal planning, workout recommendation, scheduling, progress tracking, or health and wellness. "
        "If user wants to exit, let them end the conversation."
    ),
    output_type=NonHealthDetectionOutput,
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
)

# Guardrail functions
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
        tripwire_triggered=not detection_result.final_output.is_valid,
        output_info=detection_result.final_output
    )

# Handoff agents
EscalationAgent = Agent[UserSessionContext](
    name="EscalationAgent",
    handoff_description="User wants to speak to a human coach",
    instructions=(
        "You assist users by acting as a human coach or trainer. "
        "Always acknowledge their request with empathy, "
        "provide helpful information."
    ),
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
)

NutritionExpertAgent = Agent[UserSessionContext](
    name="Nutrition Expert",
    handoff_description="Complex dietary needs like diabetes or allergies",
    instructions=(
        "You are a specialized nutrition expert focused on complex dietary needs. "
        "Address questions related to diabetes, food allergies, and medical dietary restrictions with care. "
        "Provide safe, general nutrition guidance, but always emphasize consulting a healthcare provider."
    ),
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
)

InjurySupportAgent = Agent[UserSessionContext](
    name="Injury Support",
    handoff_description="Physical limitations or injury-specific workouts",
    instructions=(
        "You specialize in assisting users with physical limitations or injuries. "
        "Offer safe, modified exercise recommendations tailored to common injuries, "
        "prioritizing safety and low-impact, rehabilitation-friendly movements. "
        "Emphasize obtaining medical clearance before starting any exercise program."
    ),
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
)

def on_escalation_handoff(ctx: RunContextWrapper[None]):
    st.session_state.messages.append({"role": "system", "content": "Handing off to escalation agent"})

def on_nutrition_Expert_handoff(ctx: RunContextWrapper[None]):
    st.session_state.messages.append({"role": "system", "content": "Handing off to nutrition expert agent"})

def on_injury_support_handoff(ctx: RunContextWrapper[None]):
    st.session_state.messages.append({"role": "system", "content": "Handing off to injury support agent"})

# Main agent
agent = Agent[UserSessionContext](
    name="Health & Wellness Agent",
    instructions=(
        "You are a friendly Health & Wellness Assistant. "
        "Support users by helping them set and analyze fitness goals, "
        "create personalized meal plans based on dietary preferences, "
        "recommend appropriate workout routines, track their progress, "
        "and schedule check-ins. Never concatenate tool names or call multiple tools in a single request. "
        "Ensure each tool call is clearly formatted and handled separately."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[analyze_goals, suggest_meal_plan, recommend_workouts, progress_tracker, smart_workout_scheduler],
    handoffs=[
        handoff(EscalationAgent, on_handoff=on_escalation_handoff),
        handoff(NutritionExpertAgent, on_handoff=on_nutrition_Expert_handoff),
        handoff(InjurySupportAgent, on_handoff=on_injury_support_handoff)
    ],
    input_guardrails=[input_detection_guardrail],
    output_guardrails=[output_detection_guardrail],
)

# Async function to process user input and stream response
async def process_input(user_input):
    if user_input.lower() == "quit":
        return "Exiting. Goodbye!"
    
    response_container = st.empty()
    full_response = ""
    try:
        result = Runner.run_streamed(agent, input=user_input, context=st.session_state.context)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                full_response += event.data.delta
                with response_container.container():
                    st.chat_message("assistant").write(full_response)
        return full_response
    except InputGuardrailTripwireTriggered:
        return "❌ Input rejected by guardrail, please try again with a valid input."
    except OutputGuardrailTripwireTriggered:
        return "⚠️ Output blocked by guardrail, please try again with a valid output."

# Streamlit UI
st.title("Health & Wellness Assistant")
st.write("Ask about fitness goals💪, meal plans🥗, workouts⛹️‍♂️, progress tracking📝, or schedule check-ins✅. Type 'quit❌' to exit.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if user_input := st.chat_input("Enter your request:"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process input and get response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(process_input(user_input))
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
    finally:
        loop.close()