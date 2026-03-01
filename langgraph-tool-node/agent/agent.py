import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from idun_agent_engine.mcp.helpers import get_langchain_tools

load_dotenv()


_tools_cache = None


async def _get_tools():
    global _tools_cache
    if _tools_cache is None:
        _tools_cache = list(await get_langchain_tools() or [])
    return _tools_cache


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


async def call_model(state: MessagesState):
    tools = await _get_tools()
    model_with_tools = model.bind_tools(tools) if tools else model
    response = await model_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}


async def call_tools(state: MessagesState):
    tools = await _get_tools()
    tool_node = ToolNode(tools)
    return await tool_node.ainvoke(state)


workflow = StateGraph(MessagesState)
workflow.add_node("call_model", call_model)
workflow.add_node("tools", call_tools)
workflow.add_edge(START, "call_model")
workflow.add_conditional_edges("call_model", tools_condition)
workflow.add_edge("tools", "call_model")
