import os

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition
from idun_agent_engine.mcp.helpers import get_langchain_tools

load_dotenv()


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide a by b. Returns an error string if b is zero."""
    if b == 0:
        return float("inf")
    return a / b


local_tools = [add, subtract, multiply, divide]

_all_tools_cache = None


async def _get_all_tools():
    global _all_tools_cache
    if _all_tools_cache is None:
        idun_tools = list(await get_langchain_tools() or [])
        _all_tools_cache = [*local_tools, *idun_tools]
    return _all_tools_cache


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


async def call_model(state: MessagesState):
    tools = await _get_all_tools()
    model_with_tools = model.bind_tools(tools) if tools else model
    response = await model_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}


async def call_tools(state: MessagesState):
    tools = await _get_all_tools()
    tools_by_name = {t.name: t for t in tools}
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        t = tools_by_name[tool_call["name"]]
        result = await t.ainvoke(tool_call["args"])
        results.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )
        )
    return {"messages": results}


workflow = StateGraph(MessagesState)
workflow.add_node("call_model", call_model)
workflow.add_node("tools", call_tools)
workflow.add_edge(START, "call_model")
workflow.add_conditional_edges("call_model", tools_condition)
workflow.add_edge("tools", "call_model")
