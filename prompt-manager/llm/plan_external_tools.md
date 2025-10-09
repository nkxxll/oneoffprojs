# Detailed Plan: External Tool Wrappers

This plan details the implementation of wrappers for the external command-line tools `tmux` and `fzf`. These wrappers will be in their own files (`tmux.go`, `fzf.go`) to encapsulate the `os/exec` logic and provide a clean, testable interface to the rest of the application.

## 1. `tmux` Wrapper (`tmux.go`)

-   **Goal:** Create a function to send text to a tmux pane.
-   **File:** `tmux.go`

### `IsTmuxAvailable()` function
-   **Signature:** `IsTmuxAvailable() bool`
-   **Logic:**
    1.  Use `exec.LookPath("tmux")` to check if the `tmux` executable exists in the system's `PATH`.
    2.  Return `true` if `err` is `nil`, `false` otherwise.

### `Send()` function
-   **Signature:** `Send(targetPane string, text string, execute bool) error`
-   **Logic:**
    1.  Define the base command: `tmux`, `send-keys`.
    2.  If `targetPane` is not empty, add `-t`, `targetPane` to the command arguments.
    3.  Add the `text` to be sent as the next argument.
    4.  If `execute` is `true`, append a final argument `C-m` to simulate pressing Enter.
    5.  Create an `exec.Cmd` with the constructed command and arguments.
    6.  Run the command using `cmd.Run()`.
    7.  Return any error from `cmd.Run()`. If the command executes but tmux returns an error (e.g., pane not found), this will be captured.

## 2. `fzf` Wrapper (`fzf.go`)

-   **Goal:** Create a function that uses `fzf` to let the user select a prompt from a list.
-   **File:** `fzf.go`

### `IsFzfAvailable()` function
-   **Signature:** `IsFzfAvailable() bool`
-   **Logic:**
    1.  Use `exec.LookPath("fzf")` to check if `fzf` is in the `PATH`.
    2.  Return `true` if `err` is `nil`, `false` otherwise.

### `Select()` function
-   **Signature:** `Select(prompts []Prompt) (uuid.UUID, error)`
-   **Logic:**
    1.  Create an `exec.Cmd` for `fzf`.
    2.  Get the command's `stdin` pipe (`cmd.StdinPipe()`).
    3.  Get the command's `stdout` pipe (`cmd.StdoutPipe()`)
    4.  Start the `fzf` command with `cmd.Start()`.
    5.  In a separate goroutine, write the prompt data to `fzf`'s stdin.
        -   The format should be easy to parse, but human-readable. A good format would be `[ID] Name - Tags`. For example: `[f81d4fae-7dec-11d0-a765-00a0c91e6bf6] Go Boilerplate - go, web`.
        -   Iterate over the `prompts` slice and write each formatted string followed by a newline to the stdin pipe.
        -   Close the stdin pipe when done to signal EOF to `fzf`.
    6.  Read the output from the stdout pipe. This will be the line selected by the user.
    7.  Wait for the command to finish with `cmd.Wait()`. If the user cancels `fzf` (e.g., with Esc), `cmd.Wait()` will return an `*exec.ExitError`. This should be handled gracefully by returning a specific error (e.g., `ErrFzfCancelled`).
    8.  Parse the selected line to extract the prompt ID (e.g., by splitting the string or using a regex).
    9.  Parse the extracted ID string into a `uuid.UUID`.
    10. Return the `uuid.UUID` and `nil` error on success.
