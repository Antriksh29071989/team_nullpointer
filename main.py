"""
MCP Server Template
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import mcp.types as types
from datetime import datetime, timedelta
import json
import requests
from requests.auth import HTTPBasicAuth
import re
import os

from dotenv import load_dotenv
load_dotenv() 

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)


@mcp.tool(
    title="Echo Tool",
    description="Echo the input text",
)
def echo(text: str = Field(description="The text to echo")) -> str:
    return text


@mcp.tool(
    title="grafana Tool",
    description="grafana the input text",
)
def grafana(text: str = Field(description="The text to echo")) -> str:
    
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

@mcp.tool(title="Jira Tool",
    description="create JIRA issue",
)
def jira(alert: str = Field(description="Create JIRA issue ") ) -> str:
    grafana_alert = json.loads(alert)
    return grafana_alert
        
    # except json.JSONDecodeError:
    #     return "Invalid JSON input"

    # # Extract server name from description if possible
    # server_match = re.search(r"server-[\w\-]+", grafana_alert.get("description", ""))
    # server_name = server_match.group(0) if server_match else "Unknown Server"

    # # Construct Jira payload
    # jira_payload = {
    #     "fields": {
    #         "project": {"key": JIRA_PROJECT_KEY},
    #         "summary": f"{grafana_alert.get('title', 'No Title')} on {server_name}",
    #         "description": f"""{grafana_alert.get('description', '')}
    #         Grafana Issue ID: {grafana_alert.get('id', '')}
    #         Severity: {grafana_alert.get('severity', '')}
    #         Status: {grafana_alert.get('status', '')}
    #         Created: {grafana_alert.get('created_at', '')}
    #         Updated: {grafana_alert.get('updated_at', '')}
    #         Tags: {', '.join(grafana_alert.get('tags', []))}
    #         Assigned to: {grafana_alert.get('assigned_to', '')} """,
    #         "issuetype": {"name": "Epic"},
    #         "labels": grafana_alert.get('tags', []) 
    #         }
    #     }
    
    # return "done"
    # # Jira REST API endpoint
    # jira_url = f"{JIRA_DOMAIN}/rest/api/2/issue/"

    # # Send request
    # response = requests.post(
    #     jira_url,
    #     auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    #     headers={"Content-Type": "application/json"},
    #     data=json.dumps(jira_payload)
    # )
    # if response.status_code == 201:
    #     issue_key = response.json()['key']
    #     return f"Jira issue created successfully! Issue URL: {JIRA_DOMAIN}/browse/{issue_key}"
    # else:
    #     return f"Failed to create Jira issue. Status: {response.status_code}, Response: {response.text}"


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