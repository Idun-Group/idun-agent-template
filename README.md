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

- Idun website: https://idunplatform.com/
- Idun repository: https://github.com/Idun-Group/idun-agent-platform

## Repository structure

- `adk-with-tool/`: ADK example agent
- `langgraph-simple/`: minimal LangGraph example agent

Each example includes:
- agent code in `agent/`
- a `requirements.txt`
- a `my_agent.yaml` configuration file
- an `.env.example` for environment setup

## Quick start

1. Pick a template folder (for example `langgraph-simple/` or `adk-with-tool/`).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create your env file from `.env.example` and set your variables.
4. Run your agent locally (for ADK projects, for example):
   ```bash
   adk web --port 8010
   ```
5. Run with Idun when ready:
   ```bash
   idun agent serve --source manager
   ```

For full platform setup and production usage, follow the Idun docs and quickstart from the official repository.
