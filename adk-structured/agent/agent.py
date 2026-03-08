from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent


class RequestInput(BaseModel):
    request_id: str = Field(description="Unique identifier for the request.")
    objective: str = Field(description="The user's main objective.")
    category: str = Field(description="The request category, such as sales, support, or ops.")
    priority: str = Field(description="Priority level such as low, medium, or high.")


class RequestOutput(BaseModel):
    request_id: str = Field(description="The request identifier from the input.")
    status: str = Field(description="Short status for the request, such as ready or needs_review.")
    category: str = Field(description="Normalized request category.")
    summary: str = Field(description="Short summary of the request.")
    next_action: str = Field(description="Recommended next action for the team.")


def suggest_next_action(category: str, priority: str) -> dict[str, str]:
    """Suggest a default next action for a request."""
    category_key = category.strip().lower()
    priority_key = priority.strip().lower()

    actions = {
        "sales": {
            "high": "Route to a sales rep for same-day follow-up.",
            "medium": "Queue for a sales follow-up within one business day.",
            "low": "Add to the sales backlog for standard outreach.",
        },
        "support": {
            "high": "Escalate to the on-call support engineer.",
            "medium": "Create a support task for the next available agent.",
            "low": "Respond with self-serve guidance and monitor for reply.",
        },
        "ops": {
            "high": "Create an urgent operations ticket and notify the team lead.",
            "medium": "Add the request to the current operations work queue.",
            "low": "Log the request for routine operations review.",
        },
    }

    default_action = "Review the request manually and assign the best owner."
    next_action = actions.get(category_key, {}).get(priority_key, default_action)
    return {"next_action": next_action}


root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="structured_request_agent",
    description="Processes structured requests and returns a structured summary.",
    instruction="""
You are a structured request processing agent.

The user input will be a JSON object that matches the input schema.
1. Read the request fields from the JSON input.
2. Use the `suggest_next_action` tool to get a recommended next step.
3. Return ONLY a JSON object that matches the output schema.

Rules:
- Keep `request_id` unchanged from the input.
- Normalize `category` to lowercase.
- Set `status` to `needs_review` when priority is `high`; otherwise set it to `ready`.
- Keep the `summary` short and clear.
""",
    tools=[suggest_next_action],
    input_schema=RequestInput,
    output_schema=RequestOutput,
    output_key="structured_request_result",
)
