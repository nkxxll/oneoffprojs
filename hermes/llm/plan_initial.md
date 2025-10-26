# Initial Plan for Hermes CLI Tool

## Project Overview
Hermes is a command-line tool for testing MCP (Model Context Protocol) servers using a
human-readable TOML configuration file. It replaces manual JSON crafting with structured test
definitions, executes tests via stdin to the MCP server, captures and prettifies output, and manages
fixtures for regression testing.

## Goals
- Human-readable TOML config for tests
- Minimal dependencies (primarily TOML parser, CLI argument handling)
- Easy maintenance and extension
- Interactive output with expandable results
- Fixture-based testing for output verification

## Technology Stack
- **Language**: JavaScript (ES modules)
- **Runtime**: Bun (for fast execution and minimal dependencies)
- **TOML Parsing**: Bun 1.3 has built-in toml parsing
- **CLI Framework**: Bun has a framework for parsing cli arguments
- **File System**: Bun's built-in fs module

## Project Structure
```
/home/nkxxll/git/oneoffprojs/hermes
├── llm/
│   └── plan_initial.md (this file)
├── src/
│   ├── index.js (main CLI entry point)
│   ├── config.js (TOML config parsing)
│   ├── runner.js (test execution logic)
│   ├── output.js (result formatting and display)
│   └── fixtures.js (fixture management)
├── package.json
├── .hermes/
│   └── fixtures/ (auto-created for fixture files)
└── README.md
```

## Development Phases

### Phase 1: Project Setup and Basic Structure
1. Initialize package.json with Bun scripts
2. Set up basic CLI argument parsing (config file path, help)
3. Create skeleton modules (index.js, config.js, etc.)
4. Implement basic TOML loading and validation

### Phase 2: Configuration Parsing
1. Define TOML schema validation
2. Parse cmd/args from config root
3. Parse [[test_runs]] arrays with nested [[test_runs.tests]]
4. Generate JSON-RPC messages from test definitions:
   - `initialize`: Standard MCP initialize request
   - `notifications/initialize`: Notification message
   - `list/tools`: Tools list request
   - `tools/call`: Tool call with params/tool+args
5. Handle defaults (jsonrpc: "2.0", auto-incrementing ids)

### Phase 3: Test Execution
1. Implement sequential test running
2. Spawn child process for `cmd` with `args` (with bun's spawn function)
3. Pipe JSON messages via stdin, capture stdout/stderr
4. Parse JSON responses (handle both success and error cases)
5. Collect results per test step

### Phase 4: Output Formatting and Display
1. Create expandable terminal output format
2. Pretty-print JSON responses
3. Show test run summaries (passed/total, new fixtures)
4. Implement interactive prompts for fixture creation

### Phase 5: Fixture Management
1. Compare actual output to saved fixtures
2. Auto-create .hermes/fixtures/ directory
3. Save fixtures in TOML format as specified
4. Load and validate existing fixtures on subsequent runs
5. Skip matching fixtures in output (expandable on demand)

### Phase 6: Error Handling and Polish
1. Add comprehensive error handling for JSON parsing, process execution
2. Implement verbose/quiet modes
3. Add test validation (malformed configs, missing tools)
4. Create example config files
5. Write unit tests for core modules

## Key Technical Considerations
- **JSON-RPC Protocol**: Ensure correct message formatting and id sequencing
- **Streaming I/O**: Handle MCP server stdin/stdout communication properly
- **TOML Flexibility**: Support both `params` and `tool`+`args` syntax for tools/call
- **Cross-Platform**: Ensure path handling works on different OSes
- **Performance**: Minimize memory usage for large test suites

## Dependencies (Minimal)
- most of the things can be handled with Bun 1.3 built-in stuff
- Potentially `chalk`: For colored terminal output (optional, can skip for minimal deps)

## Testing Strategy
- Unit tests for config parsing, message generation, fixture comparison
- Integration tests with mock MCP servers
- Manual testing with real MCP implementations

## Future Extensions (Easy to Add)
- Support for multiple MCP server configurations
- Parallel test execution
- Custom test assertions beyond fixture matching
- Export test results to various formats (JUnit XML, etc.)
- Integration with CI/CD pipelines
