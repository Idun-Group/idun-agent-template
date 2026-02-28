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
