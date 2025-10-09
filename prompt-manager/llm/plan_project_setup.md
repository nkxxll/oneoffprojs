# Detailed Plan: Project Setup and Core Data Structures

This plan details the initial setup of the Go project, including module initialization, dependency management, and the definition of the core data structures that will be used throughout the application.

## 1. Go Module Initialization

-   **Action:** Initialize the Go module.
-   **Command:** `go mod init github.com/niklas/prompt-manager`
-   **Rationale:** This creates the `go.mod` file, which is essential for managing dependencies and versioning of the project. The chosen module path follows Go conventions.

## 2. Dependency Acquisition

-   **Action:** Add all necessary third-party libraries.
-   **Commands:**
    ```bash
    go get github.com/spf13/cobra
    go get github.com/charmbracelet/bubbletea
    go get github.com/charmbracelet/lipgloss
    go get github.com/charmbracelet/bubbles
    go get github.com/google/uuid
    go get github.com/pelletier/go-toml/v2
    ```
-   **Rationale:**
    -   `cobra`: For building a powerful and modern CLI application.
    -   `bubbletea`, `lipgloss`, `bubbles`: A suite of libraries for creating sophisticated Terminal User Interfaces (TUIs).
    -   `uuid`: To generate unique identifiers for each prompt, ensuring they can be reliably referenced.
    -   `go-toml/v2`: For robust and easy handling of the TOML format for the storage file.

## 3. Core Data Structure Definition

-   **Action:** Define the `Prompt` and `Store` structs in a new file named `storage.go`.
-   **File:** `storage.go`
-   **`Prompt` Struct:**
    ```go
    package main

    import "github.com/google/uuid"

    // Prompt represents a single prompt configuration.
    type Prompt struct {
        ID   uuid.UUID `toml:"id"`
        Name string    `toml:"name"`
        Text string    `toml:"text"`
        Tags []string  `toml:"tags,omitempty"`
    }
    ```
    -   **Fields:**
        -   `ID`: A `uuid.UUID` to uniquely identify the prompt. It will be the primary key.
        -   `Name`: A short, human-readable name for the prompt (e.g., "Go Boilerplate").
        -   `Text`: The full text of the prompt.
        -   `Tags`: A slice of strings for categorizing and filtering prompts.
    -   **TOML Tags:** `toml:"..."` tags are added to control how the struct fields are encoded and decoded by the `go-toml` library. `omitempty` for tags makes the file cleaner if a prompt has no tags.

-   **`Store` Struct:**
    ```go
    // Store manages the collection of prompts and their persistence.
    type Store struct {
        filePath string
        prompts  []Prompt
    }
    ```
    -   **Fields:**
        -   `filePath`: The absolute path to the `prompts.toml` storage file.
        -   `prompts`: An in-memory slice of `Prompt` structs, which will be the working copy of the data.
