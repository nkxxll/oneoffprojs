# TUI Library Implementation Plan

## Overview
Implement a minimal TUI library in `src/tui/index.js` inspired by Bubbletea (Go) for folding/unfolding content display. The library will follow the Model-View-Update (MVU) architecture with support for commands and messages.

## Architecture Components

### 1. Model
- **Type**: Object representing application state
- **Key Properties**:
  - `items`: Array of displayable items
  - Each item has:
    - `id`: Unique identifier
    - `content`: The text content to display
    - `folded`: Boolean indicating fold state
    - `foldedContent`: Truncated/preview content when folded (optional)

### 2. Messages
- **Type**: Objects with a `type` field and associated data
- **Supported Messages**:
  - `{ type: 'toggle_fold', itemId: string }`: Toggle fold state for an item
  - `{ type: 'quit' }`: Exit the application
  - Custom messages can be extended for specific use cases

### 3. Commands
- **Type**: Functions that return promises resolving to messages
- **Purpose**: Handle asynchronous operations
- **Example**: `fetchData()` could return a command that fetches new data and sends a message with results

### 4. Core Functions

#### init()
- **Signature**: `init() -> [model, command?]`
- **Purpose**: Initialize the application state
- **Returns**: Initial model and optional initial command

#### update(model, msg)
- **Signature**: `update(model, msg) -> [newModel, command?]`
- **Purpose**: Process messages and update model state
- **Returns**: Updated model and optional command to execute

#### view(model)
- **Signature**: `view(model) -> string`
- **Purpose**: Render the current model state as displayable text
- **Returns**: Formatted string for terminal output

### 5. Runtime Loop
- **Main Loop**: 
  1. Call `view(model)` to get display string
  2. Render to terminal
  3. Wait for user input (key presses)
  4. Convert input to message
  5. Call `update(model, message)`
  6. Repeat until quit message

### 6. Integration with output.js
- **Usage in displayResults**:
  - Convert test results to TUI items
  - Initialize TUI with folded items
  - Allow user to toggle folds for detailed view
  - Handle navigation and exit

### 7. Key Features
- **Folding Logic**: 
  - Toggle between folded (summary) and unfolded (full content)
  - Keyboard shortcuts (e.g., space/enter to toggle, arrows to navigate)
- **Rendering**:
  - Simple text-based rendering
  - Indicators for fold state (▶ folded, ▼ unfolded)
- **Extensibility**: Easy to add new message types and commands

### 8. Implementation Steps
1. Define message types and model structure
2. Implement `init()`, `update()`, `view()` functions
3. Create runtime loop with input handling
4. Add folding-specific logic
5. Integrate with `src/output.js` for test result display
6. Test with sample data

### 9. Dependencies
- Node.js built-in modules for terminal I/O
- Possibly `readline` for input handling
- Keep minimal dependencies for simplicity
