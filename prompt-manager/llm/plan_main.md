# Detailed Plan: Main Entry Point

This plan details the logic in `main.go`, which serves as the application's entry point. It will be responsible for deciding whether to run the CLI or the interactive TUI based on the command-line arguments provided by the user.

## 1. `main` function structure

-   **File:** `main.go`
-   **Action:** Implement the main function logic.

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	// 1. Check for CLI arguments
	if len(os.Args) > 1 {
		// If arguments are present, assume it's a CLI command.
		// The root cobra command has a '--help' flag by default.
		// Specific commands like 'list', 'create', etc., will be handled by cobra.
		if err := Execute(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	} else {
		// 2. No arguments, launch the TUI
		// The target pane will be retrieved from the (as yet un-parsed) root command flag.
		// We need a way to get the flag value without fully executing cobra.

		// Revised approach:
		// Let cobra parse the flags first.
		// Then check if a command was executed.
	}
}
```

## 2. Revised `main` function logic

The initial logic is flawed because flags like `--target` won't be parsed if we just check `len(os.Args)`. A better approach is to let Cobra do its job and then decide what to do.

-   **Action:** Refine the `main.go` logic to correctly handle the CLI vs. TUI split.

### Step 1: Modify `cli.go`
-   In `cli.go`, the `rootCmd`'s `RunE` function will be the key.
-   **`rootCmd.RunE` Logic:**
    1.  This function runs only if no sub-command is specified.
    2.  Inside `RunE`, retrieve the value of the `--target` flag.
    3.  Call the `RunTUI(target)` function from `tui.go`.
    4.  Return the error from `RunTUI`.

### Step 2: Update `main.go`
-   The `main` function becomes much simpler.

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	// The cli.go `init()` function will have set up all commands.
	// Cobra will automatically parse arguments and flags.
	// - If a subcommand like 'list' or 'create' is used, its RunE will be executed.
	// - If NO subcommand is used, the rootCmd's RunE will be executed, which launches the TUI.
	// - If an error occurs in any command, it will be returned here.
	if err := Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "An error occurred: %v\n", err)
		os.Exit(1)
	}
}
```

## 3. Final Flow

1.  User runs `prompt-manager`.
2.  `main()` calls `cli.Execute()`.
3.  Cobra parses the arguments.
4.  **Scenario A: `prompt-manager create --name "Test"`**
    -   Cobra identifies the `create` sub-command.
    -   It executes `createCmd.RunE`.
    -   The TUI is never involved.
5.  **Scenario B: `prompt-manager` or `prompt-manager -t session:0.1`**
    -   Cobra finds no sub-command.
    -   It executes `rootCmd.RunE`.
    -   `rootCmd.RunE` reads the `-t` flag value.
    -   `rootCmd.RunE` calls `RunTUI()` with the target.
    -   The interactive TUI starts.
6.  Any error from any `RunE` function propagates up to `main`, where it is printed, and the program exits with a non-zero status code.

```