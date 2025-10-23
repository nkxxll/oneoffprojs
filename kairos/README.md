# Kairos

Kairos is a client-server application designed for time tracking using the **MCP protocol**. Its primary goal is to run a **MCP server on a Raspberry Pi** that keeps track of time entries using **timew**, a C++ timekeeping tool. The system supports interaction through a client or through an LLM via a standard I/O proxy.

## Features

- **Server**: Maintains time tracking entries and exposes control through the MCP protocol.
- **Client**: Provides a direct interface to manage time entries without needing an LLM.
- **LLM Integration**: With a standard I/O proxy, the server can be controlled by language models like Claude Code.
- **Backend**: Uses `timew` for reliable timekeeping.

## TODOs

- [ ] start a timer
  - [ ] the names are clearly defined
  - [ ] the server starts a time keeping with `timew start <name>`
  - [ ] start a timer in the past
- [ ] stop a timer
  - [ ] stop a timer in the past
  - [ ] stop a timer from the server
- [ ] modify an entry
  - [ ] given an id and a new end time modify an entry
  - [ ] given an id and a new start time modify an entry
  - [ ] given an id and a new start and end time modify an entry
- [ ] remove an entry by id

## Structure

- `./client/client.go` is the entry point for the mcp client
  - has the client only code which start the mcp client and connects to the server
- `./server/server.go` is the server entry point which uses
  - has the server only code that starts the server and exposes it to broadcast on a port defined by
    a flag or env var
- `./tmcp/mcp.go` to start a mcp server
  - has the shared mcp logic if there is any between the client and the server
- `./timew/timew.go` should handle the command calls to the `timew` cli tools
  - this package should also define the shared types for timew
