import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

load_dotenv()


class AgentState(TypedDict):
    user_input: str
    plan: str
    response: str


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def analyze_step(state: AgentState) -> AgentState:
    """Step 1: create a short plan before answering."""
    planning_prompt = (
        "You are planning an answer.\n"
        "Create a concise 2-3 bullet point plan to answer the user request.\n\n"
        f"User request: {state['user_input']}"
    )
    plan = llm.invoke(planning_prompt).content
    return {"plan": str(plan)}


def answer_step(state: AgentState) -> AgentState:
    """Step 2: generate final response from the plan."""
    answer_prompt = (
        "You are a helpful assistant.\n"
        "Use the plan to answer the user clearly and briefly.\n\n"
        f"Plan:\n{state['plan']}\n\n"
        f"User request: {state['user_input']}"
    )
    response = llm.invoke(answer_prompt).content
    return {"response": str(response)}


workflow = StateGraph(AgentState)
workflow.add_node("analyze", analyze_step)
workflow.add_node("answer", answer_step)
workflow.add_edge(START, "analyze")
workflow.add_edge("analyze", "answer")
workflow.add_edge("answer", END)

graph = workflow.compile()
