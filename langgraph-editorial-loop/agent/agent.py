import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

load_dotenv()


class AgentState(MessagesState, total=False):
    topic: str
    context: str
    draft: str
    status: Literal["needs_research", "drafting", "reviewing", "done"]
    loop_count: int


class ReviewDecision(BaseModel):
    decision: Literal["needs_research", "drafting", "done"] = Field(
        description=(
            "Select 'needs_research' if facts are missing. "
            "Select 'drafting' to rewrite. "
            "Select 'done' if the draft is complete."
        )
    )
    feedback: str = Field(description="Feedback/instructions for the next step.")


research_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
writer_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
reviewer_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
reviewer_structured = reviewer_model.with_structured_output(ReviewDecision)


def extract_topic(state: AgentState) -> dict[str, str]:
    """Extract the topic from the user's message."""
    topic = str(state["messages"][-1].content)
    return {"topic": topic}


def researcher(state: AgentState) -> dict[str, str]:
    topic = state.get("topic", "")
    context = state.get("context", "")
    prompt = (
        f"Gather key facts about: {topic}.\n"
        f"Current context you already know: {context or 'None'}\n\n"
        "Provide a concise bulleted summary with factual details."
    )
    response = str(research_model.invoke(prompt).content)
    new_context = f"{context}\n\n{response}".strip() if context else response
    return {"context": new_context, "status": "drafting"}


def writer(state: AgentState) -> dict[str, str]:
    prompt = (
        "Write a cohesive, engaging article based strictly on this context:\n"
        f"{state.get('context', '')}\n\n"
        "Current draft to improve (if any):\n"
        f"{state.get('draft') or 'None'}\n\n"
        "Ensure your response is a complete article and does not cut off."
    )
    response = str(writer_model.invoke(prompt).content)
    return {"draft": response, "status": "reviewing"}


def reviewer(state: AgentState) -> dict[str, object]:
    prompt = (
        f"Evaluate this draft against the original topic: {state.get('topic', '')}.\n\n"
        "Draft:\n"
        f"{state.get('draft', '')}\n\n"
        "Decide if it needs more research, another rewrite, or is done.\n"
        "Return a structured decision with clear feedback."
    )
    decision = reviewer_structured.invoke(prompt)

    context = state.get("context", "")
    if decision.decision != "done":
        feedback_line = f"Reviewer Feedback: {decision.feedback}"
        context = f"{context}\n\n{feedback_line}".strip() if context else feedback_line

    loop_count = int(state.get("loop_count", 0)) + 1
    status = "done" if loop_count >= 3 else decision.decision
    return {"context": context, "status": status, "loop_count": loop_count}


def finalize(state: AgentState) -> dict[str, list[AIMessage]]:
    """Return the final draft as an AI message."""
    draft = state.get("draft", state.get("context", ""))
    return {"messages": [AIMessage(content=str(draft))]}


def route_graph(state: AgentState) -> str:
    return state.get("status", "done")


workflow = StateGraph(AgentState)
workflow.add_node("extract_topic", extract_topic)
workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)
workflow.add_node("reviewer", reviewer)
workflow.add_node("finalize", finalize)

workflow.add_edge(START, "extract_topic")
workflow.add_edge("extract_topic", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    route_graph,
    {
        "needs_research": "researcher",
        "drafting": "writer",
        "done": "finalize",
    },
)
workflow.add_edge("finalize", END)

graph = workflow
