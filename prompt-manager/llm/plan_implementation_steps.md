# Implementation Plan: Prompt Manager

This document outlines the step-by-step plan for implementing the **Prompt Manager** application, based on the prior research. The implementation will be broken down into distinct phases, starting with the data layer and progressively building up to the command-line and terminal user interfaces.

## Step 1: Project Setup and Core Data Structures

**Goal:** Initialize the project, add dependencies, and define the core data structures.

1.  **Initialize Go Module:** Run `go mod init github.com/user/prompt-manager` to create the `go.mod` file.
2.  **Add Dependencies:** Use `go get` to add the necessary libraries:
    *   `github.com/spf13/cobra` for the CLI.
    *   `github.com/charmbracelet/bubbletea` for the TUI.
    *   `github.com/charmbracelet/lipgloss` for TUI styling.
    *   `github.com/charmbracelet/bubbles` for TUI components (list, textinput).
    *   `github.com/google/uuid` for generating unique prompt IDs.
    *   `github.com/pelletier/go-toml/v2` for TOML file parsing in the storage layer.
3.  **Create `storage.go`:**
    *   Define the `Prompt` struct with `ID`, `Name`, `Text`, and `Tags` fields.
    *   Define the `Store` struct that will manage the list of prompts and the file path.

## Step 2: Storage Layer

**Goal:** Implement the logic for creating, reading, updating, and deleting prompts from a local file.

1.  **Implement in `storage.go`:**
    *   **File Path Logic:** Create a function to determine the storage file path (e.g., `~/.config/prompt-manager/prompts.toml`). It should create the directory if it doesn't exist.
    *   **`NewStore()`:** A constructor that initializes the store, determines the file path, and loads initial data.
    *   **`Load()` method:** Reads the TOML file from disk and unmarshals it into `[]Prompt`.
    *   **`Save()` method:** Marshals the current `[]Prompt` slice into TOML and writes it to the file.
    *   **CRUD Methods:** Implement `GetAll()`, `Add(p Prompt)`, `Get(id string)`, `Update(id string, p Prompt)`, and `Remove(id string)`. These methods will modify the in-memory prompt list and then call `Save()` to persist the changes.

## Step 3: External Tool Wrappers

**Goal:** Create dedicated wrappers for interacting with `tmux` and `fzf` to isolate the `os/exec` logic.

1.  **Create `tmux.go`:**
    *   Implement `Send(target, text string, execute bool) error`.
    *   This function will construct and run the `tmux send-keys` command.
    *   It will include a check to see if the `tmux` executable is available in the system's PATH.
    *   The `execute` flag will control whether `C-m` is appended to the command.
2.  **Create `fzf.go`:**
    *   Implement `Select(prompts []Prompt) (Prompt, error)`.
    *   This function will check if the `fzf` executable is available.
    *   It will pipe a formatted list of prompt names to the `fzf` process.
    *   It will read the selection from `fzf`'s stdout and return the corresponding `Prompt` struct.
    *   It will handle cancellation (e.g., user pressing Esc) gracefully.

## Step 4: Command-Line Interface (CLI)

**Goal:** Build the non-interactive CLI for managing prompts as defined in the `README.md`.

1.  **Create `cli.go`:**
    *   Initialize the `cobra` root command.
    *   **`create` command:** Add flags for `--name`, `--text`, `--tags`. This command will instantiate a new `Prompt`, call the `storage.Add()` method.
    *   **`list` command:** (Corresponds to `display` in README). Lists all prompts in a formatted table.
    *   **`update` command:** Takes an ID argument and flags for fields to update. Calls `storage.Update()`.
    *   **`remove` command:** Takes an ID argument and calls `storage.Remove()`.
    *   **`search` command:** Takes a keyword argument and filters prompts by name or tag.
2.  **Update `main.go`:**
    *   Set up the main function to execute the `cobra` root command.

## Step 5: Terminal User Interface (TUI)

**Goal:** Build the interactive TUI for browsing, selecting, and managing prompts.

1.  **Create `tui.go`:**
    *   **Main Model:** Define a `tea.Model` struct that holds the application state: `list.Model` for the prompt list, `textinput.Model` for forms, the current list of prompts, error messages, etc.
    *   **`Init()`:** Return a command to load the initial prompts from the `Store`.
    *   **`Update()`:** Implement the main logic loop.
        *   Handle list navigation (up/down keys).
        *   Handle prompt selection (Enter key): On selection, call `tmux.Send()` with the chosen prompt's text.
        *   Handle CRUD inputs (`c` for create, `d` for delete, `e` for edit), switching the view/state of the TUI to a form.
        *   Handle form input and submission, calling the appropriate `storage` methods and then reloading the main list.
    *   **`View()`:** Render the UI based on the current state. Use `lipgloss` for styling.
        *   If in the list view, render the `list.View()`.
        *   If in a form view, render the form inputs.
        *   Display help text and status messages.

## Step 6: Tying It All Together

**Goal:** Finalize the application's entry point to handle both CLI and TUI modes.

1.  **Refine `main.go`:**
    *   The main function will check if any arguments or specific sub-commands were passed.
    *   If sub-commands (like `create`, `list`) are present, it will execute the CLI via `cobra`.
    *   If no arguments are provided, it will launch the interactive TUI by creating and running a new `tea.Program`.
    *   A `--target` (`-t`) flag on the root command will be used to specify the tmux target for both modes.
