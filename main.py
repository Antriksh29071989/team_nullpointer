from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import json
import requests
from requests.auth import HTTPBasicAuth
import re
import os

from dotenv import load_dotenv
load_dotenv() 

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)
 

@mcp.tool(title="grafana issue",
    description="Tool Description for the grafana")
async def get_grafana_issues() -> str:
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


JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

@mcp.tool()
async def create_jira_issue(grafana_alert_json: str) -> str:
    """
    MCP tool to create a Jira issue from a Grafana alert JSON.

    Args:
        grafana_alert_json (str): JSON string of Grafana alert

    Returns:
        str: Jira issue URL or error message

    """

    try:
        grafana_alert = json.loads(grafana_alert_json)
        
    except json.JSONDecodeError:
        return "Invalid JSON input"

    # Extract server name from description if possible
    server_match = re.search(r"server-[\w\-]+", grafana_alert.get("description", ""))
    server_name = server_match.group(0) if server_match else "Unknown Server"

    # Construct Jira payload
    jira_payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": f"{grafana_alert.get('title', 'No Title')} on {server_name}",
            "description": f"""
{grafana_alert.get('description', '')}

Grafana Issue ID: {grafana_alert.get('id', '')}
Severity: {grafana_alert.get('severity', '')}
Status: {grafana_alert.get('status', '')}
Created: {grafana_alert.get('created_at', '')}
Updated: {grafana_alert.get('updated_at', '')}
Tags: {', '.join(grafana_alert.get('tags', []))}
Assigned to: {grafana_alert.get('assigned_to', '')}
""",
            "issuetype": {"name": "Epic"},
            "labels": grafana_alert.get('tags', []) 
        }
    }

    # Jira REST API endpoint
    jira_url = f"{JIRA_DOMAIN}/rest/api/2/issue/"

    # Send request
    response = requests.post(
        jira_url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Content-Type": "application/json"},
        data=json.dumps(jira_payload)
    )

    if response.status_code == 201:
        issue_key = response.json()['key']
        return f"Jira issue created successfully! Issue URL: {JIRA_DOMAIN}/browse/{issue_key}"
    else:
        return f"Failed to create Jira issue. Status: {response.status_code}, Response: {response.text}"


# Confluence credentials
CONFLUENCE_DOMAIN = os.getenv("CONFLUENCE_DOMAIN")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = "antriksh29071989"  # optional: limit search to a space

@mcp.tool()
async def search_confluence_solution(title: str) -> str:
    """
    Search Confluence for a solution to a given issue title or description snippet.

    Args:
        issue_title (str): The Jira/Grafana issue title or description snippet.

    Returns:
        str: Solution content if found, otherwise a message.
    """
    # REST API endpoint
    url = f"{CONFLUENCE_DOMAIN}/rest/api/content/search"

    # Use 'params' to let requests handle encoding
    params = {
        "cql": f'title ~ "{title}" OR text ~ "{title}"',  # search title or content
        "limit": 5,
        "expand": "body.storage"
    }

    response = requests.get(
        url,
        auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        headers={"Accept": "application/json"},
        params=params
    )

    if response.status_code != 200:
        return f"Failed to search Confluence. Status: {response.status_code}, Response: {response.text}"

    data = response.json()
    results = data.get("results", [])

    if not results:
        return "No solution found in Confluence."

    # Return first match
    page = results[0]
    page_title = page.get("title")
    page_url = f"{CONFLUENCE_DOMAIN}/pages/{page['id']}"
    content = page.get("body", {}).get("storage", {}).get("value", "")

    # Return formatted string
    return f"Solution found: {page_title}\nURL: {page_url}\nContent:\n{content}"

if __name__ == "__main__":
    try:
        print("started")
        # mcp.run(transport="stdio")  # or stdioz
        mcp.run(transport="streamable-http")     # enable streaming if supporteds
    except Exception as e:
        # Log to stderr instead of stdout
        import traceback
        import sys
        traceback.print_exc(file=sys.stderr)
        # Exit with non-zero code
        sys.exit(1)
