"""
MCP Server Template
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field

import mcp.types as types

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)


@mcp.tool(
    title="Echo Tool",
    description="Echo the input text",
)
def echo(text: str = Field(description="The text to echo")) -> str:
    return text


@mcp.tool(title="grafana issue",
    description="Tool Description for the grafana")
def get_grafana_issues() -> str:
    """Get dummy Grafana issue for demonstration.
    
    Returns a sample Grafana issue.
    """
    # Generate one dummy issue
    now = datetime.now()
    
    issue = {
        "id": "GRAF-001",
        "title": "High CPU Usage Alert",
        "type": "Alert",
        "severity": "High",
        "status": "Open",
        "description": "CPU usage has exceeded 90% for the last 15 minutes on server-web-01",
        "created_at": (now - timedelta(hours=2)).isoformat(),
        "updated_at": (now - timedelta(minutes=30)).isoformat(),
        "assigned_to": "ops-team@company.com",
        "tags": ["infrastructure", "performance", "urgent"]
    }
    
   # Return as JSON string
    return json.dumps(issue)


@mcp.resource(
    uri="greeting://{name}",
    description="Get a personalized greeting",
    name="Greeting Resource",
)
def get_greeting(
    name: str,
) -> str:
    return f"Hello, {name}!"







@mcp.prompt("")
def greet_user(
    name: str = Field(description="The name of the person to greet"),
    style: str = Field(description="The style of the greeting", default="friendly"),
) -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")