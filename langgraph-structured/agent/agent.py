import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

load_dotenv()


class InputState(TypedDict):
    request_id: str
    objective: str
    context: dict[str, str]
    constraints: list[str]
    priority: str


class InternalState(InputState):
    analysis: str
    risk_level: str
    actions: list[str]
    status: str
    summary: str


class OutputState(TypedDict):
    request_id: str
    status: str
    summary: str
    actions: list[str]
    risk_level: str


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def analyze_request(state: InputState) -> dict[str, str]:
    constraints = ", ".join(state["constraints"]) if state["constraints"] else "none"
    prompt = (
        "You are an internal operations analysis agent.\n"
        "Analyze the request and provide:\n"
        "1) a concise analysis paragraph\n"
        "2) a risk level as one of LOW, MEDIUM, HIGH\n\n"
        f"Request ID: {state['request_id']}\n"
        f"Objective: {state['objective']}\n"
        f"Priority: {state['priority']}\n"
        f"Constraints: {constraints}\n"
        f"Context: {state['context']}\n\n"
        "Format exactly as:\n"
        "RISK_LEVEL: <LOW|MEDIUM|HIGH>\n"
        "ANALYSIS: <text>"
    )
    text = str(model.invoke(prompt).content)
    risk_level = "MEDIUM"
    analysis = text
    for line in text.splitlines():
        if line.startswith("RISK_LEVEL:"):
            candidate = line.split(":", 1)[1].strip().upper()
            if candidate in {"LOW", "MEDIUM", "HIGH"}:
                risk_level = candidate
        if line.startswith("ANALYSIS:"):
            analysis = line.split(":", 1)[1].strip()
    return {"risk_level": risk_level, "analysis": analysis}


def build_plan(state: InternalState) -> dict[str, object]:
    prompt = (
        "You are an internal system planning agent.\n"
        "Based on the analysis, provide exactly 3 concrete action items.\n"
        "Each action must be short and implementation-oriented.\n\n"
        f"Objective: {state['objective']}\n"
        f"Priority: {state['priority']}\n"
        f"Risk level: {state['risk_level']}\n"
        f"Analysis: {state['analysis']}\n"
        f"Constraints: {state['constraints']}\n\n"
        "Return each action on its own line, with no numbering."
    )
    raw_actions = str(model.invoke(prompt).content)
    actions = [line.strip("- ").strip() for line in raw_actions.splitlines() if line.strip()]
    actions = actions[:3] if actions else ["Define implementation steps", "Execute safely", "Validate results"]

    status = "needs_review" if state["risk_level"] == "HIGH" else "ready"
    summary = (
        f"Objective '{state['objective']}' analyzed with {state['risk_level']} risk. "
        f"Generated {len(actions)} actions for internal execution."
    )
    return {"actions": actions, "status": status, "summary": summary}


workflow = StateGraph(
    InternalState,
    input_schema=InputState,
    output_schema=OutputState,
)
workflow.add_node("analyze_request", analyze_request)
workflow.add_node("build_plan", build_plan)
workflow.add_edge(START, "analyze_request")
workflow.add_edge("analyze_request", "build_plan")
workflow.add_edge("build_plan", END)
