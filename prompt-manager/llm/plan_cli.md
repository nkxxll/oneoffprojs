# Detailed Plan: Command-Line Interface (CLI)

This plan outlines the implementation of the non-interactive command-line interface using the `cobra` library. The CLI will provide commands for managing prompts directly from the shell. All CLI-related code will reside in `cli.go`.

## 1. Root Command Setup

-   **File:** `cli.go`
-   **Action:** Initialize the root command and a persistent flag for the tmux target.
-   **`rootCmd`:**
    -   A `*cobra.Command` variable representing the base command (e.g., `prompt-manager`).
    -   `Use: "prompt-manager"`
    -   `Short: "A tool for managing and using prompts with tmux."`
-   **Persistent Flag:**
    -   Add a persistent string flag `--target` (shorthand `-t`) to `rootCmd`.
    -   This flag will store the target tmux pane (e.g., `session:window.pane`) and will be available to all sub-commands.
-   **`Execute()` function:**
    -   A public function `Execute()` that will be called from `main.go`. It simply calls `rootCmd.Execute()`.

## 2. `create` Sub-command

-   **Action:** Create a command to add a new prompt.
-   **`createCmd`:**
    -   `Use: "create"`
    -   `Short: "Create a new prompt"`
    -   **Run Logic (`RunE`):**
        1.  Instantiate the `Store` by calling `NewStore()`.
        2.  Retrieve flag values for name, text, and tags.
        3.  Perform basic validation (e.g., name and text are not empty).
        4.  Create a new `Prompt` struct.
        5.  Generate a new `uuid.UUID` for the `ID`.
        6.  Call `store.Add()` with the new prompt.
        7.  Print a confirmation message to the user (e.g., "Prompt 'Go Boilerplate' created with ID ...").
-   **Flags:**
    -   `--name` (string, required): The name of the prompt.
    -   `--text` (string, required): The content of the prompt.
    -   `--tags` (stringSlice): Comma-separated tags for the prompt.

## 3. `list` Sub-command

-   **Action:** Create a command to display all existing prompts.
-   **`listCmd`:**
    -   `Use: "list"`
    -   `Short: "List all prompts"`
    -   **Run Logic (`RunE`):**
        1.  Instantiate the `Store`.
        2.  Call `store.GetAll()` to get all prompts.
        3.  If the list is empty, print a message like "No prompts found."
        4.  If prompts exist, format them into a clean, readable table using the `text/tabwriter` package.
        5.  The table should include columns for `ID`, `Name`, and `Tags`.

## 4. `update` Sub-command

-   **Action:** Create a command to modify an existing prompt.
-   **`updateCmd`:**
    -   `Use: "update [ID]"`
    -   `Short: "Update an existing prompt"`
    -   `Args: cobra.ExactArgs(1)` to ensure an ID is provided.
    -   **Run Logic (`RunE`):**
        1.  Instantiate the `Store`.
        2.  Parse the ID argument into a `uuid.UUID`.
        3.  Call `store.Get()` to fetch the existing prompt. If not found, return an error.
        4.  Check which flags were set by the user using `cmd.Flags().Changed("flag-name")`.
        5.  For each changed flag, update the corresponding field in the fetched prompt struct.
        6.  Call `store.Update()` with the modified prompt struct.
        7.  Print a confirmation message.
-   **Flags:**
    -   `--name` (string): New name for the prompt.
    -   `--text` (string): New text for the prompt.
    -   `--tags` (stringSlice): New set of tags (will replace old tags).

## 5. `remove` Sub-command

-   **Action:** Create a command to delete a prompt.
-   **`removeCmd`:**
    -   `Use: "remove [ID]"`
    -   `Short: "Remove a prompt"`
    -   `Args: cobra.ExactArgs(1)`
    -   **Run Logic (`RunE`):**
        1.  Instantiate the `Store`.
        2.  Parse the ID argument into a `uuid.UUID`.
        3.  Call `store.Remove()` with the ID.
        4.  Print a confirmation message.

## 6. `search` Sub-command

-   **Action:** Create a command to find prompts by keyword.
-   **`searchCmd`:**
    -   `Use: "search [keyword]"`
    -   `Short: "Search for prompts by name or tag"`
    -   `Args: cobra.ExactArgs(1)`
    -   **Run Logic (`RunE`):**
        1.  Instantiate the `Store`.
        2.  Get the keyword from the arguments.
        3.  Call `store.GetAll()` and filter the results in-memory.
        4.  A prompt matches if the keyword is a substring of its `Name` or if the keyword matches one of its `Tags` (case-insensitive).
        5.  Print the matching prompts using the same tabular format as the `list` command.

## 7. Command Registration

-   **Action:** Add all sub-commands to the `rootCmd`.
-   **`init()` function in `cli.go`:**
    -   Call `rootCmd.AddCommand(createCmd, listCmd, updateCmd, removeCmd, searchCmd)`.
    -   Define all flags for the sub-commands within this function.
