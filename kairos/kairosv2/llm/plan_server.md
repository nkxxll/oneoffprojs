# Plan for Kairos v2 MCP Server

## Overview

Develop an MCP server using Bun that communicates with the timew time-tracking tool on a Raspberry Pi via SSH commands. This stateless approach replaces the previous unstable MCP connection, allowing reliable time tracking from any computer with SSH access to the Pi.

## Architecture

The server will consist of three main modules:

- **index.ts**: Main server file defining the MCP server, registering tools and resources for timew operations.
- **types.ts**: TypeScript definitions for configuration, command structures, and MCP tool inputs.
- **commandComposer.ts**: Module responsible for composing SSH commands from MCP arguments, handling configuration, and executing or logging commands based on run mode.

Configuration will be stored in a TOML file named `kairosv2.toml` located in the kairos config directory (`~/.kairos/`).

The server will support a "dry" command-line option that logs and returns SSH commands as strings instead of executing them, useful for testing and debugging.

## Modules Detail

### types.ts
Define the following key types:
- `KairosConfig`: Interface for configuration including Pi host, username, SSH key path, etc.
- `TimewCommand`: Union type representing different timew operations (start, stop, summary, track, etc.) with their respective arguments.
- `McpToolInput`: Types for MCP tool inputs, corresponding to timew command parameters.
- `CommandResult`: Type for command execution results, including success status and output.

### commandComposer.ts
Implement functions to:
- Load and parse the `kairosv2.toml` configuration file.
- Compose SSH commands in the format: `ssh user@host timew [command] [args]`.
- Execute SSH commands using Bun's process API or a shell execution library.
- In dry mode, return the composed command string instead of executing it.
- Handle SSH errors and timeouts gracefully.

### index.ts
- Import and initialize the MCP server using the @modelcontextprotocol/sdk.
- Register MCP tools for common timew operations:
  - `timew_start`: Start tracking time for a task.
  - `timew_stop`: Stop the current time tracking.
  - `timew_summary`: Get a summary of tracked time.
  - `timew_track`: Track time for a specific period.
- Each tool handler will:
  1. Parse MCP input arguments.
  2. Call the command composer to generate the SSH command.
  3. Execute or log the command based on the mode.
  4. Return the result in the required MCP format.

## CLI Integration

Add command-line argument parsing to support the "dry" option. Use a library like `commander` or Bun's built-in argument handling to detect `--dry` or `-d` flag, setting the execution mode accordingly.

## Implementation Steps

1. Set up the project structure with the three modules.
2. Implement configuration loading and TOML parsing (using a library like `@iarna/toml`).
3. Define all necessary types in `types.ts`.
4. Build the command composition and execution logic in `commandComposer.ts`.
5. Register timew-specific tools in `index.ts`, replacing the placeholder tools.
6. Integrate CLI option parsing for dry run mode.
7. Test the server with various timew commands, verifying SSH execution and dry run output.
8. Add error handling for SSH connection issues and invalid timew commands.
9. Document the configuration file format and tool usage.

## Dependencies

- `@modelcontextprotocol/sdk`: For MCP server implementation.
- `zod`: For input validation (already imported).
- `@iarna/toml`: For configuration file parsing.
- `commander` or similar: For CLI argument parsing (if needed).

This plan provides a modular, maintainable structure for the Kairos v2 MCP server, focusing on simplicity and reliability through SSH-based communication.
