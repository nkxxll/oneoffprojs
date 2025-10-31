# Command Palette Implementation Plan

## Current State
- Command palette toggle is implemented via Ctrl+P key binding
- Basic input box is shown when `showCommand` is true
- No command parsing or execution logic exists yet

## Completion Steps

### 1. Input Handling
- Add state to store the current command input
- Implement onChange handler for the input component to update the command state
- Handle Enter key to execute the command
- Handle Escape key to close the command palette

### 2. Command Parsing
- Create a command parser function that recognizes:
  - `add [files]`: Git add command (default to `git add .` if no files specified)
  - `commit <message>`: Git commit with message
  - `push`: Git push to current branch
- Support basic argument parsing for file paths in add command
- Add command validation and error messages for invalid syntax

### 3. Command Execution
- Implement async functions for each git command using the Bash tool
- Execute commands in background to avoid blocking the UI
- Update the data state after successful command execution to refresh StatusView and DiffView
- Show loading state during command execution

### 4. UI Improvements
- Display command suggestions/autocomplete as user types
- Show command execution feedback (success/error messages)
- Add command history with up/down arrow navigation
- Style the command palette with better positioning and appearance

### 5. Error Handling
- Catch and display git command errors
- Handle network issues for push command
- Provide user-friendly error messages
- Allow retry for failed operations

### 6. Integration
- Ensure commands update the git status and diff data
- Refresh the UI after each command completes
- Maintain keyboard focus and navigation flow

## Command Specifications

### Add Command
```
add [files...]
```
- If no files specified: `git add .`
- If files specified: `git add <files>`
- Refresh status after execution

### Amend

```
commit --amend <message>
# or
commit --amend --no-edit
```

### Commit Command
```
commit <message>
```
- Execute: `git commit -m "<message>"`
- Require message parameter
- Refresh status and diff after execution

### Push Command
```
push
```
- Execute: `git push`
- or execute push force but with and additional dialogue: `git push`
- Refresh status after execution
- Handle authentication prompts if needed
