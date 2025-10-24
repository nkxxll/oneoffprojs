# Client Rework Plan: Splitting CLI into MCP Proxy and HTTP CLI

## Overview

The current `client.go` implements a CLI that directly connects to the MCP server using the MCP protocol. This needs to be split into two separate executables:

1. **MCP Proxy Server**: A continuously running server that maintains the MCP connection and exposes HTTP endpoints for tool calls.
2. **CLI Client**: A command-line application that sends HTTP requests to the proxy server and displays responses.

This separation allows the MCP connection to persist across multiple CLI invocations, improving efficiency and reliability.

## Architecture

```
CLI Commands (start, stop, modify, etc.)
    ↓ HTTP Requests (JSON)
MCP Proxy Server (HTTP Server)
    ↓ MCP Protocol
MCP Server (Kairos Time Tracking)
```

- **MCP Proxy Server**: Runs continuously, maintains MCP session, handles HTTP requests by calling MCP tools
- **CLI Client**: Stateless, invoked per command, sends HTTP requests, parses responses
- **Shared Schemas**: JSON schemas for request/response structures used by both components

## Components

### 1. MCP Proxy Server (`client/proxy/`)

- HTTP server (e.g., using net/http or echo)
- MCP client connection management
- Tool call routing from HTTP endpoints to MCP tools
- Error handling and response formatting
- Configuration for MCP server URL

### 2. CLI Client (`client/cli/`)

- Cobra-based CLI structure (similar to current)
- HTTP client for sending requests to proxy server
- Request building from command flags/args
- Response parsing and output formatting
- Configuration for proxy server URL

### 3. Shared Schemas (`client/shared/`)

- JSON request/response structures
- Go structs with JSON tags
- Validation logic
- Common types (e.g., time formats, error responses)

## Implementation Steps

1. **Create Directory Structure**

   ```
   client/
   ├── proxy/          # MCP proxy server
   │   ├── main.go
   │   └── server.go
   ├── cli/            # CLI client
   │   ├── main.go
   │   └── commands.go
   ├── shared/         # Shared schemas
   │   ├── types.go
   │   └── schemas.go
   └── client.go       # Keep for reference, remove later
   ```

2. **Define Shared Schemas**
   - Request structs for each tool call (start_timer, stop_timer, etc.)
   - Response structs with tool output and error handling
   - Common types for time parsing, IDs, etc.
   - The schemas can be derived from the types in `./tmcp/mcp.go` and `./timew/timew.go`

3. **Implement MCP Proxy Server**
   - Set up HTTP server with endpoints matching tool names
   - Initialize MCP client and maintain session
   - Parse HTTP requests into MCP tool calls
   - Format MCP responses into HTTP responses
   - Handle connection errors and reconnection logic

4. **Implement CLI Client**
   - Adapt existing Cobra commands to build HTTP requests instead of MCP calls
   - Use shared schemas to construct request bodies
   - Send requests to proxy server
   - Parse and display responses

5. **Configuration Management**
   - Both components need server URLs (proxy URL for CLI, MCP URL for proxy)
   - Environment variables or config files
   - Default localhost ports

6. **Error Handling**
   - Proxy server errors (MCP connection issues)
   - HTTP client errors (connection to proxy)
   - Tool execution errors
   - Consistent error response format

7. **Testing**
   - Unit tests for shared schemas
   - Integration tests for proxy server
   - End-to-end tests with both components

## Shared Request/Response Schemas

### Tool Call Request

```json
{
  "tool_name": "start_timer",
  "arguments": {
    "name": "task_name",
    "start_time": "2023-01-01T00:00:00Z"
  }
}
```

### Tool Call Response

```json
{
  "success": true,
  "output": "Timer started: task_name",
  "error": null
}
```

Or on error:

```json
{
  "success": false,
  "output": "",
  "error": "Failed to start timer: <reason>"
}
```
