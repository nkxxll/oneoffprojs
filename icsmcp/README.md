# ICS MCP Server

A Model Context Protocol (MCP) server that provides tools for creating, managing, and exporting `.ics` calendar files.  
The goal is to enable an LLM client (for example, Claude Desktop) to create structured calendar data through simple RPC commands.

## Motivation

Large language models are good at generating structured text, but they often struggle to maintain strict schema consistency for complex objects such as calendar events.  
The ICS MCP Server addresses this by exposing a small set of structured, composable tools that handle validation and state on the server side. This allows the LLM to focus on intent rather than syntax.

Instead of forcing the model to construct an entire `.ics` file in one step, this design allows it to:

1. Create individual events safely (`createEvent`)
2. Build a complete calendar from multiple validated events (`createCalendar`)
3. Retrieve, inspect, or clear the temporary working state as needed

This approach improves reliability, flexibility, and modularity when interacting with calendar data.

## Design Overview

The server follows a multi-tool architecture where each tool performs one clear, self-contained action.  

### Tools

**1. createEvent**  
Creates a new event object and appends it to the temporary state.  
Missing or malformed fields are handled gracefully by the tool (for example, defaulting an end time if only a start time is provided).

**2. createCalendar**  
Generates an `.ics` file from all events currently stored in the temporary state.  
Accepts a filename and produces the corresponding `.ics` file.

Might be extended with:

**3. addAlert**
Adds an alert to a specific calendar event...

...and other similar tools.

---

## Example Workflow

1. The LLM calls `createEvent` one or more times to define events.  
2. Once ready, the LLM calls `createCalendar("schedule.ics")` to export the final file.  
3. The resulting `.ics` file can then be accessed, used, or shared by the client.

This simple two-step flow is easy for an LLM to use reliably, while still allowing fine-grained validation and error recovery on the server side.

## Contributing

Contributions are welcome.  
If you would like to add new features or improve the tool design, please open an issue or pull request describing your proposed change.  
When contributing, aim to keep the following principles:

- Each tool should remain small and focused on a single action.
- Server state should stay minimal and easy to inspect.
- The LLM interface should be explicit, with predictable parameter names and outputs.

## License

MIT License

