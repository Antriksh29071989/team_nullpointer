# JIRA and Meeting Management MCP Server

This project implements a Model Context Protocol (MCP) server that provides tools for connecting to JIRA, creating and managing tickets, and scheduling meetings. The server follows the [official MCP documentation](https://modelcontextprotocol.io/docs/develop/build-server) standards.

## Features

### JIRA Tools
- **JIRA Connection Management**: List available connections and get projects
- **JIRA Ticket Management**: Comprehensive ticket operations (create, get, update, comment)

### Meeting Tools
- **Schedule Meetings**: Create meetings with attendees, time, and location
- **List Meetings**: View upcoming meetings with filtering options

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have Python 3.10 or higher installed.

## Configuration

### For Claude Desktop

1. Copy the configuration to your Claude Desktop config file:
```bash
# On macOS
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# On Windows
copy claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json
```

2. Update the paths in the config file to match your system.

3. Restart Claude Desktop.

### JIRA Setup

JIRA connections are established during server startup using environment variables. You'll need:
- A JIRA instance URL (e.g., `https://yourcompany.atlassian.net`)
- A JIRA username or email
- A JIRA API token (generate from your JIRA account settings)

Set these environment variables:
```bash
JIRA_CONNECTION_MAIN_URL=https://yourcompany.atlassian.net
JIRA_CONNECTION_MAIN_USERNAME=your.email@company.com
JIRA_CONNECTION_MAIN_TOKEN=your_jira_api_token_here
```

See [JIRA_CONFIGURATION.md](JIRA_CONFIGURATION.md) for detailed setup instructions.

## Usage Examples

### Listing JIRA Connections
```
List all available JIRA connections
```

### Creating a JIRA Ticket
```
Use JIRA ticket tool with operation "create", connection "main", and details '{"project_key": "PROJ", "issue_type": "Bug", "summary": "Login issue", "description": "Users cannot log in", "assignee": "john.doe", "priority": "High"}'
```

### Scheduling a Meeting
```
Schedule a meeting titled "Sprint Planning" starting at "2024-01-15T10:00:00" for 60 minutes with attendees ["team@company.com", "manager@company.com"] and description "Plan next sprint tasks"
```

### Getting JIRA Projects
```
Get all JIRA projects from connection "main"
```

### Getting JIRA Ticket Details
```
Use JIRA ticket tool with operation "get", connection "main", and ticket key "PROJ-123"
```

### Updating a JIRA Ticket
```
Use JIRA ticket tool with operation "update", connection "main", ticket key "PROJ-123", and details '{"summary": "Fixed login issue", "assignee": "jane.doe", "comment": "Issue resolved in latest deployment"}'
```

### Adding a Comment to JIRA Ticket
```
Use JIRA ticket tool with operation "comment", connection "main", ticket key "PROJ-123", and details '{"comment": "This is a new comment"}'
```

## Available Tools

### JIRA Tools
1. `list_jira_connections` - List available JIRA connections
2. `get_jira_projects` - Get projects from a JIRA connection
3. `jira_ticket` - Comprehensive ticket management (create, get, update, comment)

### Meeting Tools
1. `schedule_meeting` - Schedule new meetings
2. `list_meetings` - List upcoming meetings

## Architecture

The server uses the FastMCP framework which automatically generates tool definitions from Python type hints and docstrings. This makes it easy to maintain and extend the functionality.

### Key Components

- **FastMCP Server**: Main server instance handling MCP protocol
- **JIRA Connection Management**: Stores and manages multiple JIRA connections
- **HTTP Client**: Async HTTP client for JIRA API calls
- **Error Handling**: Comprehensive error handling and logging

## Development

### Running the Server
```bash
python mcp_server.py
```

### Testing with Claude Desktop
1. Configure Claude Desktop with the provided config file
2. Restart Claude Desktop
3. Look for the tools icon in Claude Desktop
4. Test the tools with natural language commands

### Logging
The server logs to stderr (required for STDIO-based MCP servers). Check Claude Desktop logs for debugging:
```bash
# On macOS
tail -f ~/Library/Logs/Claude/mcp*.log
```

## Security Notes

- API tokens are stored in memory only during the session
- All JIRA API calls use HTTPS
- No sensitive data is logged
- Connections are validated before use

## Troubleshooting

### Common Issues

1. **Server not showing in Claude Desktop**
   - Check the config file syntax
   - Ensure absolute paths are used
   - Restart Claude Desktop completely

2. **JIRA connection failures**
   - Verify credentials and URL
   - Check API token permissions
   - Ensure JIRA instance is accessible

3. **Tool execution errors**
   - Check Claude Desktop logs
   - Verify server is running without errors
   - Test with simple commands first

### Debug Mode
Enable debug logging by modifying the logging level in `mcp_server.py`:
```python
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
```

## Contributing

1. Follow the MCP standards from the official documentation
2. Use type hints and docstrings for automatic tool generation
3. Test with Claude Desktop before submitting changes
4. Ensure all logging goes to stderr, not stdout

## License

This project is provided as an example implementation of the Model Context Protocol.
