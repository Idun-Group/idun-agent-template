from pathlib import Path

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from agent.copy_logic import copy_requested_file

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "source_docs"
TARGET_DIR = BASE_DIR / "target_docs"


def copy_file_node(state: MessagesState):
    if not state.get("messages"):
        return {"messages": [AIMessage(content="No input received. Try: copy test.txt")]}

    user_text = str(state["messages"][-1].content)
    result = copy_requested_file(user_text, SOURCE_DIR, TARGET_DIR)
    return {"messages": [AIMessage(content=result)]}


workflow = StateGraph(MessagesState)
workflow.add_node("copy_file", copy_file_node)
workflow.add_edge(START, "copy_file")
workflow.add_edge("copy_file", END)
