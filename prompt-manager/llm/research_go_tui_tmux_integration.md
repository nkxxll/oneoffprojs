# Research: Building a Go TUI with Tmux Integration

This document outlines the research and proposed approach for building the **Prompt Manager**, a terminal-based application written in Go. The goal is to create a tool that provides both a command-line interface (CLI) and a terminal user interface (TUI) for managing a collection of prompts and streaming them into a Tmux pane.

## 1. Core Components & Libraries

Based on the project requirements, the following Go libraries and external tools are recommended.

### CLI: `cobra`
For the command-line interface, `cobra` is the ideal library. It is designed for creating powerful, modern CLI applications with a nested command structure, similar to `git` or `docker`. This directly matches the usage examples in the `README.md` (`prompt-cli create`, `prompt-cli update`, etc.).

- **Features**: Sub-command management, flag parsing (e.g., `-n` for name, `-t` for target), automatic help generation, and scaffolding tools.
- **Implementation**: We would define commands like `createCmd`, `removeCmd`, etc., in `cli.go` and register them in the main application entry point.

### TUI: `bubbletea`
As specified in the `README.md`, `bubbletea` will be used for the interactive TUI. It's a powerful, Elm-inspired framework that allows for building stateful and responsive terminal applications.

- **Architecture**: It uses a Model-View-Update (MVU) pattern.
    - **Model**: A struct holding the application's state (e.g., list of prompts, cursor position, current view).
    - **View**: A function that renders the UI as a string based on the current model state.
    - **Update**: A function that handles events (e.g., key presses, data loading) and updates the model accordingly.
- **Implementation**: The TUI would feature a list of prompts. Users could select a prompt to trigger a Tmux command, or enter other views to create, update, or delete prompts. This logic will reside in `tui.go`.

### Fuzzy Finder: `fzf`
To provide a fast and intuitive way to select from a potentially large list of prompts, integrating the command-line fuzzy finder `fzf` is a great approach.

- **Integration**: A Go program can execute `fzf` as a subprocess using the `os/exec` package.
    1. The Go application will write the list of prompt names to the `stdin` of the `fzf` process.
    2. `fzf` will handle the interactive filtering in the terminal.
    3. The selected prompt name is read back from the `stdout` of the `fzf` process.
- **Implementation**: A helper function in `fzf.go` will encapsulate this logic, taking a list of prompts and returning the one selected by the user.

**Note:** if `fzf` is not installed the program will fallback to simple substring searching with
`bubbletea`.

### Tmux Integration
The core feature of streaming prompts requires communication with Tmux. This is achievable by calling the `tmux` command-line tool from Go.

- **Mechanism**: Use `os/exec` to run `tmux` commands. The most relevant command is `send-keys`.
- **Command**: `tmux send-keys -t <target> '<prompt_text>' C-m`
    - `-t <target>`: Specifies the target Tmux window or pane (e.g., `@6` as in the `README.md` example).
    - `'<prompt_text>'`: The prompt content to be "typed" into the terminal.
    - `C-m`: Sends a carriage return (Enter key) to execute the prompt. This can be turned on or
    off by a command-line argument
- **Implementation**: A function `SendToTmux(target, text string)` in `tmux.go` will be created to handle this interaction safely.

### Storage
A simple file-based storage system is sufficient for managing the prompts. JSON is a good choice due to its human-readability and excellent support in Go's standard library.

- **Structure**: A single `prompts.json` file containing a list of prompt objects. Each object would have fields like `id`, `name`, `text`, and `tags`.
- **Implementation**: The `storage.go` file will define the `Prompt` struct and contain all the logic for CRUD (Create, Read, Update, Delete) operations.
    - `LoadPrompts() ([]Prompt, error)`: Reads and parses the JSON file.
    - `SavePrompts([]Prompt) error`: Writes the current list of prompts back to the file.
    - Functions for adding, updating, and removing prompts from the list.

## 2. Proposed Project Structure

The file structure outlined in the `README.md` is logical and maps well to the researched components.

- **`main.go` (or `promptcli.go`)**: The main entry point. It will parse initial arguments to decide whether to launch the CLI (`cobra`) or the interactive TUI (`bubbletea`).
- **`cli.go`**: Contains all `cobra` command definitions (`create`, `remove`, `update`, etc.). These functions will call the underlying logic in `storage.go` and `tmux.go`.
- **`tui.go`**: Implements the `bubbletea` application. The TUI's model will hold the application state, and its `Update` function will react to user input, calling functions from `storage.go`, `tmux.go`, and `fzf.go`.
- **`storage.go`**: Defines the `Prompt` struct and handles all file I/O for reading from and writing to the `prompts.toml` file. Which is in the standard local data location for the operating system.
- **`tmux.go`**: Provides a simple function to send text to a specified Tmux target.
- **`fzf.go`**: Contains the helper function to run the `fzf` process and get the user's selection.

## 3. Conclusion

The proposed project is highly feasible. The chosen Go libraries (`cobra`, `bubbletea`) are well-documented and perfectly suited for the task. Integration with external command-line tools like `fzf` and `tmux` is straightforward using Go's standard `os/exec` package. The plan provides a clear path forward for implementation.
