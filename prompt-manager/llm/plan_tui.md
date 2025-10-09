# Detailed Plan: Terminal User Interface (TUI)

This plan details the implementation of the interactive TUI using the `bubbletea` framework. The TUI will be the default mode when the application is run without sub-commands. All TUI-related code will be in `tui.go`.

## 1. Main TUI Model

-   **File:** `tui.go`
-   **Action:** Define the main `tea.Model` for the TUI application.
-   **`tuiModel` struct:**
    -   `store *Store`: A pointer to the data store.
    -   `list list.Model`: The `bubbles/list` component to display prompts.
    -   `form *Form`: A custom struct to manage create/edit forms.
    -   `state viewState`: An enum (`listView`, `formView`) to control the current view.
    -   `err error`: To hold and display any errors that occur.
    -   `tmuxTarget string`: The target pane for sending prompts.

## 2. `bubbles/list` Component Setup

-   **Action:** Configure the list component for displaying prompts.
-   **Item Delegate:**
    -   Create a custom `itemDelegate` that implements `list.ItemDelegate`.
    -   `Render()` method: Define how a single list item is rendered. It should display the prompt's `Name` and `Tags` using `lipgloss` for styling.
    -   `Height()` and `Spacing()`: Set the dimensions for list items.
-   **List Initialization:**
    -   In the TUI constructor (`NewTUI`), create an instance of `list.New()`.
    -   Pass the items (prompts from the store), the custom `itemDelegate`, a width, and a height.
    -   Set the title of the list (e.g., "Your Prompts").
    -   Configure keybindings for help, quit, etc.

## 3. Form Management (`Form` struct)

-   **Action:** Create a struct and methods to handle data entry for creating and editing prompts.
-   **`Form` struct:**
    -   `id *uuid.UUID`: A pointer to the ID. `nil` for create, non-`nil` for edit.
    -   `name textinput.Model`: A `bubbles/textinput` for the prompt name.
    -   `text textarea.Model`: A `bubbles/textarea` for the prompt text.
    -   `tags textinput.Model`: A `bubbles/textinput` for comma-separated tags.
    -   `focusIndex int`: To track which form field is currently active.
-   **`NewCreateForm()` / `NewEditForm(p Prompt)`:** Functions to create a pre-populated form for editing or an empty one for creating.
-   **`Focus()` / `Blur()`:** Methods to manage focus on the form fields.
-   **`Update()` / `View()`:** Methods that will be called by the main `tuiModel`'s `Update` and `View` when in `formView`.

## 4. `tea.Model` Interface Implementation

-   **`Init()`:**
    -   **Signature:** `(m tuiModel) Init() tea.Cmd`
    -   **Logic:** Return `nil`. The initial loading of prompts will be handled by the constructor.

-   **`Update()`:**
    -   **Signature:** `(m tuiModel) Update(msg tea.Msg) (tea.Model, tea.Cmd)`
    -   **Logic:** This is the core logic loop. Use a `switch` on the `msg` type.
        -   **`tea.KeyMsg`:**
            -   Check the `m.state`.
            -   **If `listView`:**
                -   `enter`: Get the selected prompt. Call `tmux.Send()` with the prompt's text and the `tmuxTarget`. Quit the TUI.
                -   `c`: Switch `m.state` to `formView` and initialize a new create form.
                -   `e`: Get the selected prompt. Switch `m.state` to `formView` and initialize an edit form with the prompt's data.
                -   `d`: Get the selected prompt. Call `store.Remove()`. Reload the list items.
                -   `q` / `ctrl+c`: Quit the application.
                -   Otherwise, pass the message to the `list.Update()` method to handle navigation.
            -   **If `formView`:**
                -   `esc`: Switch back to `listView`.
                -   `enter`: If the last field is focused, submit the form. Call `store.Add()` or `store.Update()`. Reload the list and switch back to `listView`.
                -   `tab`: Cycle focus between form fields.
                -   Otherwise, pass the message to the focused form field's `Update` method.
        -   **`tea.WindowSizeMsg`:** Update the dimensions of the list and other components.

-   **`View()`:**
    -   **Signature:** `(m tuiModel) View() string`
    -   **Logic:**
        -   Check `m.state`.
        -   **If `listView`:** Return the result of `m.list.View()`.
        -   **If `formView`:** Return the result of `m.form.View()`.
        -   Append a help/status bar at the bottom, rendered with `lipgloss`, showing common keybindings and the current error message if `m.err` is not `nil`.

## 5. TUI Entry Point

-   **Action:** Create a function to launch the TUI.
-   **Function:** `RunTUI(targetPane string)`
-   **Logic:**
    1.  Check if `fzf` and `tmux` are available using the wrapper functions. If not, return an error.
    2.  Instantiate the `Store`.
    3.  Create the initial `tuiModel`, passing the store and `targetPane`.
    4.  Create a new `tea.Program` with the model.
    5.  Run the program: `p.Run()`. Return any error from the run.
