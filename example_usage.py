"""
Example usage of the JIRA and Meeting Management MCP Server

This file demonstrates how to use the MCP server tools programmatically.
Note: In practice, these tools are typically used through Claude Desktop or other MCP clients.
"""

import asyncio
import json
from mcp_server import (
    list_jira_connections, get_jira_projects, jira_ticket, 
    schedule_meeting, list_meetings
)


async def example_jira_workflow():
    """Example workflow for JIRA operations."""
    print("=== JIRA Workflow Example ===\n")
    
    # 1. List available JIRA connections
    print("1. Listing available JIRA connections...")
    connections_result = await list_jira_connections()
    print(f"Connections: {connections_result}\n")
    
    # 2. Get available projects (assuming 'main' connection exists)
    print("2. Getting JIRA projects...")
    projects_result = await get_jira_projects("main")
    print(f"Projects: {projects_result}\n")
    
    # 3. Create a new ticket
    print("3. Creating a new JIRA ticket...")
    create_details = json.dumps({
        "project_key": "PROJ",
        "issue_type": "Bug",
        "summary": "Example bug report",
        "description": "This is an example bug report created via MCP server",
        "assignee": "john.doe",
        "priority": "Medium",
        "labels": ["example", "mcp"]
    })
    ticket_result = await jira_ticket(
        operation="create",
        connection_name="main",
        details=create_details
    )
    print(f"Ticket creation result: {ticket_result}\n")
    
    # 4. Get ticket details
    print("4. Getting ticket details...")
    ticket_details = await jira_ticket(
        operation="get",
        connection_name="main",
        ticket_key="PROJ-123"
    )
    print(f"Ticket details: {ticket_details}\n")
    
    # 5. Update the ticket
    print("5. Updating the ticket...")
    update_details = json.dumps({
        "summary": "Updated example bug report",
        "comment": "This ticket was updated via MCP server"
    })
    update_result = await jira_ticket(
        operation="update",
        connection_name="main",
        ticket_key="PROJ-123",
        details=update_details
    )
    print(f"Update result: {update_result}\n")
    
    # 6. Add a comment
    print("6. Adding a comment...")
    comment_details = json.dumps({
        "comment": "This is a standalone comment added via MCP server"
    })
    comment_result = await jira_ticket(
        operation="comment",
        connection_name="main",
        ticket_key="PROJ-123",
        details=comment_details
    )
    print(f"Comment result: {comment_result}\n")


async def example_meeting_workflow():
    """Example workflow for meeting operations."""
    print("=== Meeting Workflow Example ===\n")
    
    # 1. Schedule a meeting
    print("1. Scheduling a meeting...")
    meeting_result = await schedule_meeting(
        title="Sprint Planning Meeting",
        start_time="2024-01-15T10:00:00",
        duration_minutes=60,
        attendees=["team@company.com", "manager@company.com", "stakeholder@company.com"],
        description="Plan tasks for the next sprint",
        location="Conference Room A"
    )
    print(f"Meeting scheduled: {meeting_result}\n")
    
    # 2. List meetings
    print("2. Listing upcoming meetings...")
    meetings_list = await list_meetings(
        start_date="2024-01-15",
        end_date="2024-01-20"
    )
    print(f"Meetings: {meetings_list}\n")


async def main():
    """Main example function."""
    print("JIRA and Meeting Management MCP Server - Example Usage\n")
    print("Note: This is a demonstration. In practice, these tools are used through Claude Desktop.\n")
    
    # Run JIRA workflow
    await example_jira_workflow()
    
    # Run meeting workflow
    await example_meeting_workflow()
    
    print("=== Example Complete ===")
    print("\nTo use these tools in practice:")
    print("1. Install Claude Desktop")
    print("2. Configure the MCP server in Claude Desktop")
    print("3. Use natural language commands like:")
    print("   - 'Connect to JIRA with URL https://company.atlassian.net'")
    print("   - 'Create a bug ticket in project PROJ with title Login Issue'")
    print("   - 'Schedule a meeting tomorrow at 2 PM for 1 hour'")


if __name__ == "__main__":
    asyncio.run(main())
