# MCP Server Implementation Plan

## Overview

The MCP server in Kairos will expose time tracking functionality through the Model Context Protocol, allowing clients (including LLMs via proxies) to interact with the time tracking system. The core logic will be implemented in `./tmcp/mcp.go`, with potential shared components between client and server for protocol handling.

## Deps

- `go-mcp`

## Core Components

### 1. MCP Protocol Handling

- Define MCP tool definitions for each time tracking operation
- Implement message parsing and response formatting
- Handle MCP initialization and capability negotiation

### 2. Tool Definitions

Based on the TODO items, implement the following MCP tools:

- `start_timer`:
  - Start a new timer with a given name
  - start timer in the past
- `stop_timer`:
  - Stop the currently running timer
  - also stop timer in the past
- `modify_entry`:
  - Modify the start time of an existing entry by ID
  - Modify the end time of an existing entry by ID
  - Modify both start and end times of an entry by ID
- `remove_entry`: Delete an entry by ID
- `summary`: use the summary command
  - week
  - day
  - month
- `export`: export the entries either for
  - the last week
  - the last day
  - from now till \<datetime\>
  - from start datetime till end datetime

### 3. Shared Structures

- Define request/response types for each tool
- Create error handling structures for MCP responses

### 5. Server-Specific Logic

- Tool handler functions that execute timew commands
- State management for active timers (if needed)
- MCP server initialization and tool registration

## Implementation Steps

1. Add each tool handler incrementally, starting with start/stop timer
2. Integrate with timew package for actual time tracking operations
3. Add proper error handling and validation
