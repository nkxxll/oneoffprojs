# Plan for Implementing the Timew Package

## Overview
The `timew` package serves as a Go wrapper around the `timew` CLI tool, providing programmatic access to time tracking functionality. It handles command execution, output parsing, and defines shared data types used by both the client and server components.

## Core Responsibilities
- Execute `timew` CLI commands and capture their output
- Parse command outputs into structured Go data types
- Provide high-level functions for time tracking operations (start, stop, modify, remove)
- Define shared types for time entries and operations
- Handle error cases and edge conditions from CLI interactions

## Shared Data Types
- `TimeEntry`: Struct representing a single time tracking entry with fields for ID, start time, end time, tags, and duration
- `TimeRange`: Struct for representing time intervals with start and end times
- `CommandResult`: Struct to encapsulate CLI command execution results, including success status, output, and error messages
- `TimeEntryList`: Slice of TimeEntry with methods for filtering and sorting
- Enumeration types for operation statuses (e.g., active, completed, error)

## Key Functions
- `StartTimer(name string, startTime *time.Time) error`: Start a new timer with optional start time
- `StopTimer(endTime *time.Time) error`: Stop the current timer with optional end time
- `ModifyEntry(id string, startTime *time.Time, endTime *time.Time) error`: Modify existing entry times
- `RemoveEntry(id string) error`: Delete an entry by ID
- `Summary`: use the summary command
  - week
  - day
  - month
- `Export`: export the entries either for
  - the last week
  - the last day
  - from now till \<datetime\>
  - from start datetime till end datetime

## Command Execution Strategy
- Use Go's `exec` package to run `timew` commands
- Capture stdout and stderr separately for better error handling
- Implement timeout handling for long-running commands
- Parse JSON or structured output when available, fall back to text parsing

## Error Handling
- Define custom error types for different failure scenarios (command not found, invalid arguments, parsing errors)
- Provide detailed error messages that include original CLI output
- Handle concurrent access issues if multiple operations occur simultaneously

## Testing Considerations
- Unit tests for individual functions with mocked CLI execution
- Integration tests that actually call timew CLI
- Test data fixtures with sample timew outputs for parsing validation
- Edge case testing for invalid inputs and system failures

## Dependencies
- Standard library packages: `os/exec`, `time`, `strconv`, `strings`
- Minimal external dependencies to keep the package lightweight
- Consider using a command execution library if complex piping or redirection is needed

## Integration Points
- Called by MCP server handlers for time tracking operations
- Results consumed by client for display and user interaction
- Shared types used across client-server communication for consistency
