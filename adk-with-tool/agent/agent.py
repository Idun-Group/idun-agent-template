from google.adk.agents import LlmAgent
from idun_agent_engine.mcp.helpers import get_adk_tools

tools = get_adk_tools()

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='webagents',
    description="Agent that can give information.",
    instruction="You are a helpful assistant that can help with giving information. Use tool fetch (ONLY IF AVAILABLE) to get information from an url.",
    tools=tools,
)
