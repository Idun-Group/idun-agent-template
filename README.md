# Idun Agent Templates

This repository contains simple agent templates and examples you can run with the **Idun Agent Platform**.

It is a starter repo for teams who want to build agents with:

- **ADK**
- **LangGraph**
- (and extend to LangChain-based patterns)

## Goal of this repository

Use this repo as a practical starting point to:

- bootstrap new agent projects quickly
- test local agent behavior
- connect agents to Idun for deployment and governance

## Link with Idun Platform

The templates in this repo are designed to run with Idun.

With Idun Platform, your agent can be exposed as a production-ready service with features like API standardization, observability, memory, and governance controls.

- Idun website: [idunplatform.com](https://idunplatform.com/)
- Idun documentation: [docs.idunplatform.com](https://docs.idunplatform.com)
- Idun repository: [Idun Agent Platform](https://github.com/Idun-Group/idun-agent-platform)

## Repository structure

- `adk-tool/`: ADK example agent with tools
- `adk-structured/`: ADK example agent with structured input and output
- `langgraph-simple/`: minimal LangGraph example agent
- `langgraph-tool/`: LangGraph agent using Idun tools (manual tool-call workaround)
- `langgraph-tool-node/`: LangGraph agent using Idun tools with `ToolNode`
- `langgraph-tool-local/`: LangGraph agent combining local math tools + Idun tools
- `langgraph-structured/`: structured input/output LangGraph internal system agent
- `langgraph-editorial-loop/`: LangGraph multi-step researcher/writer/reviewer loop agent
- `langgraph-copy-paste/`: simple LangGraph file copy example using local folders

Each example includes:

- agent code in `agent/`
- a `requirements.txt`
- a `my_agent.yaml` configuration file
- an `.env.example` for environment setup

## Quick start

1. Pick a template folder (for example `adk-tool/`, `adk-structured/`, `langgraph-simple/`, `langgraph-tool/`, `langgraph-tool-local/`, `langgraph-structured/`, `langgraph-editorial-loop/`, or `langgraph-copy-paste/`).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create your env file from `.env.example` and set your variables.
4. Run your agent locally (for ADK projects, for example):

   ```bash
   adk web --port 8010
   ```

## Connect to Idun Platform

To connect any template to the **Idun Manager** for centralized management, guardrails, observability, memory, and MCP tool governance:

1. **Create the agent** in the [Manager UI](https://docs.idunplatform.com/manager/tutorial).
2. **Copy the API key** from the **Agent Detail > API Integration** tab.
3. **Set environment variables:**

   ```bash
   export IDUN_MANAGER_HOST=http://localhost:8000
   export IDUN_AGENT_API_KEY=<your-api-key>
   ```

4. **Run in managed mode:**

   ```bash
   idun agent serve --source manager
   ```

The agent fetches its config from the platform. Any guardrails, observability, memory, or MCP tools you configure in the UI are automatically applied.

## Documentation

- [Quickstart](https://docs.idunplatform.com/quickstart)
- [Frameworks](https://docs.idunplatform.com/frameworks)
- [Guardrails](https://docs.idunplatform.com/guardrails)
- [Observability](https://docs.idunplatform.com/observability)
- [Tool Governance](https://docs.idunplatform.com/tool-governance)

---

Need help with a custom agent setup? [Book a call](https://calendar.app.google/RSzm7EM5VZY8xVnN9) or email [contact@idun-group.com](mailto:contact@idun-group.com).
