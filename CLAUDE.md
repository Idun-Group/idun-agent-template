# CLAUDE.md

Guidance for AI agents working in this repository.

## Purpose

This repository contains runnable agent templates/examples for Idun Platform, including ADK and LangGraph starters.

## Working rules

1. Keep examples simple, runnable, and easy to copy.
2. Prefer small, focused changes over large refactors.
3. Preserve existing folder patterns:
   - one folder per template/example
   - `agent/` for source code
   - `requirements.txt` for dependencies
   - `my_agent.yaml` for Idun config
   - `.env.example` for required environment variables
4. Never commit secrets. Only update `.env.example`, not real `.env` values.
5. Keep instructions aligned with Idun Platform:
   - https://idunplatform.com/
   - https://github.com/Idun-Group/idun-agent-platform

## README maintenance (required)

When adding a new agent template/example folder, you must also update `README.md` in the same change:

- add the new folder to the "Repository structure" section
- add or adjust quick-start steps if the run command differs
- keep README wording simple and straightforward

If a change impacts how users run examples, update `README.md` before finishing.

## Quality checks before finishing

- verify paths and commands in docs are correct
- ensure the template can run with listed dependencies
- keep naming consistent with existing examples

## LangGraph + Idun tool pattern

When building LangGraph agents that use Idun tools (`get_langchain_tools`), follow this pattern:

1. Use `MessagesState` and standard tool-routing nodes:
   - model node (`call_model`)
   - tools node (`tools` via `ToolNode`)
   - edges: `START -> call_model -> tools_condition -> tools -> call_model`
2. Do not call `asyncio.run()` at module import time in agent modules.
   - Idun/FastAPI can import the module inside an active event loop.
3. Load Idun tools with `await get_langchain_tools()` inside async node execution (or via an async cache helper).
4. Prefer async node functions with `ainvoke` when awaiting tool/model calls.
5. If caching tools, use an async-safe module cache helper (e.g., `_get_tools`) rather than starting a new loop.

Reference implementation shape:

```python
async def _get_tools():
    ...

async def call_model(state: MessagesState):
    tools = await _get_tools()
    response = await model.bind_tools(tools).ainvoke(state["messages"])
    return {"messages": [response]}

async def call_tools(state: MessagesState):
    tools = await _get_tools()
    return await ToolNode(tools).ainvoke(state)
```

<!-- IDUN-KNOWLEDGE-START -->
<!-- Auto-synced from idun-knowledge vault — last synced: 2026-03-22 18:34 -->

# Idun Agent Template — Vault Context

## Project Context
Reusable agent templates for Idun Platform, each extracted from real client deployments. Templates are the fastest path from "I need an agent for X" to a production-ready, governed agent running on Idun Platform.

**New templates** should be documented in the idun-knowledge vault under `product/specs/`.

## Architecture

# Idun Platform — Architecture Overview

## What Idun Platform Does
Idun Platform is the operating layer enterprises use to deploy, orchestrate, govern, and observe AI agents in production.

## Core Capabilities
1. **Agent Deployment** — Package and deploy agents to any infrastructure
2. **Orchestration** — Multi-agent coordination, workflow management
3. **Governance** — Policies, permissions, approval workflows, guardrails
4. **Observability** — Traces, logs, metrics, cost tracking per agent
5. **Security** — Role-based access control, secrets management, audit logs
6. **Memory** — Shared and per-agent memory management
7. **Integrations** — Connectors to enterprise systems (CRM, ERP, etc.)
8. **Lifecycle Management** — Versioning, rollback, staging

## Repository
- **Main repo**: https://github.com/Idun-Group/idun-agent-platform
- **Landing page**: separate repo

## Architecture Principles
1. **Open-source first** — Core platform is open-source
2. **Self-hostable** — Must run on customer infrastructure (sovereignty)
3. **API-first** — Every feature accessible via API, UI is a consumer
4. **Agent-agnostic** — Works with any agent framework
5. **Observable by default** — Every agent action is traced and logged
6. **Secure by design** — RBAC, encryption, audit trails from day one

## Tech Stack
> TODO: Fill in by running Claude Code in the idun-agent-platform repo to analyze the actual codebase

## Architecture Decision Records
See `adrs/` directory. Template: [[templates/adr-template]]

## Development Conventions

# Development Conventions

## Git Conventions

### Branch Naming
- `feat/short-description` — New features
- `fix/short-description` — Bug fixes
- `refactor/short-description` — Code refactoring
- `docs/short-description` — Documentation
- `chore/short-description` — Build, CI, dependencies

### Commit Messages (Conventional Commits)
type(scope): short description

Types: feat, fix, refactor, docs, test, chore, ci

### Pull Requests
- Title matches commit convention
- Description includes: What, Why, How to test
- At least 1 reviewer required
- CI must pass before merge

## Code Style
> TODO: Extract from repo linting config

- Meaningful variable/function names (no abbreviations)
- Docstrings for public functions
- Keep functions under 50 lines
- Prefer composition over inheritance

## Testing
- Write tests for new features (unit + integration)
- Coverage target: 80%+
- Descriptive test names: test_should_reject_invalid_policy_config

## Claude Code Usage
- Always read CLAUDE.md before starting work
- Use /plan for complex features before coding
- Reference ADRs for architecture decisions
- Reference [[brand/brand-identity]] for any UI work
- Reference [[brand/design-tokens.json]] for colors, spacing, typography

## Brand & Design

- **Primary color**: #6C63FF (Idun Purple)
- **Dark background**: #1A1A2E
- **Accent red**: #E94560 (alerts, destructive)
- **Success green**: #4CAF50
- **Font**: Inter or system sans-serif; JetBrains Mono for code

### Voice
- Expert but approachable, technical without jargon overload
- Use "AI agents" not "bots"; "Governance" not "management"; "Deploy" not "install"
- Never: "cutting-edge", "revolutionary", "just"

<!-- IDUN-KNOWLEDGE-END -->
