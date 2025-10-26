# Hermes

Hermes is a command-line tool for testing MCP (Model Context Protocol) servers using a human-readable TOML configuration file. It replaces manual JSON crafting with structured test definitions, executes tests via stdin to the MCP server, captures and prettifies output, and manages fixtures for regression testing.

## Installation

Ensure you have Bun installed. Then, you can run the tool directly or install globally.

## Usage

```bash
bun src/index.js [options] <config-file>
```

Options:
- `-h, --help`: Show help message
- `-v, --verbose`: Enable verbose output
- `-q, --quiet`: Enable quiet mode

## Goals

- Human-readable TOML config for tests
- Minimal dependencies (primarily Bun's built-in features)
- Easy maintenance and extension
- Interactive output with expandable results
- Fixture-based testing for output verification

## Configuration Format

The configuration is a TOML file specifying the MCP server command and test runs.

```toml
cmd = "path/to/mcp-server"
args = ["arg1", "arg2"]

[[test_runs]]
name = "basic test run"

  [[test_runs.tests]]
  type = "initialize"
  # Optional params as TOML table
  [test_runs.tests.params]
  protocolVersion = "2025-06-18"
  capabilities = {}
  [test_runs.tests.params.clientInfo]
  name = "hermes-client"
  version = "1.0.0"

  [[test_runs.tests]]
  type = "notifications/initialized"

  [[test_runs.tests]]
  type = "list/tools"

  [[test_runs.tests]]
  type = "tools/call"
  # Either use params table
  [test_runs.tests.params]
  name = "greeter"
  [test_runs.tests.params.arguments]
  name = "tim"

  # Or use tool and args
  # tool = "greeter"
  # args = { name = "tim" }
```

### Supported Test Types
- `initialize`: Sends initialize request
- `notifications/initialized`: Sends initialized notification
- `list/tools`: Lists available tools
- `tools/call`: Calls a tool with params or tool/args

## Fixtures

Fixtures are automatically saved in `.hermes/fixtures/` as JSON files. When a test run matches an existing fixture, the output is suppressed unless verbose mode is enabled. New fixtures are created automatically for tests without existing fixtures.

## Example

See `example-config.toml` for a sample configuration.
