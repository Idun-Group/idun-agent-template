import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph

load_dotenv()


class AgentState(MessagesState):
    plan: str


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def analyze_step(state: AgentState) -> dict[str, str]:
    """Step 1: create a short plan before answering."""
    user_message = str(state["messages"][-1].content)
    plan_prompt = [
        SystemMessage(content="You are planning an answer."),
        HumanMessage(
            content=(
                "Create a concise 2-3 bullet point plan to answer the user message.\n\n"
                f"User message: {user_message}"
            )
        ),
    ]
    plan = llm.invoke(plan_prompt).content
    return {"plan": str(plan)}


def answer_step(state: AgentState) -> dict[str, list[AIMessage]]:
    """Step 2: generate final response from the plan."""
    answer_prompt = [
        SystemMessage(content="You are a helpful assistant."),
        *state["messages"],
        HumanMessage(
            content=(
                "Use this plan to answer clearly and briefly.\n\n"
                f"Plan:\n{state['plan']}"
            )
        ),
    ]
    response = llm.invoke(answer_prompt).content
    return {"messages": [AIMessage(content=str(response))]}


workflow = StateGraph(AgentState)
workflow.add_node("analyze", analyze_step)
workflow.add_node("answer", answer_step)
workflow.add_edge(START, "analyze")
workflow.add_edge("analyze", "answer")
workflow.add_edge("answer", END)

graph = workflow.compile()

