# Plan: Fix TUI Keybindings in Filter Mode

## 1. Problem Analysis

The user reported that in the TUI (`tui.go`), when the prompt list is in filter mode (activated by `/`), standard key presses **like** `c`, `e`, and `enter` are being intercepted by the application's global keybindings instead of being used as input for the filter.

The root cause is in the `updateListView` function. The current logic checks for custom keybindings (`c` for create, `e` for edit, etc.) in a `switch` statement *before* passing the key press message to the `list.Model.Update` method. This means that even when the list component is expecting text input for its filter, our custom keybindings hijack those key presses.

## 2. Proposed Solution

The `updateListView` function needs to be refactored to be aware of the list's state. The `list.Model` provides a `FilterState()` method which returns the current filtering status (e.g., `list.Filtering`).

The new logic will be as follows:

1.  Inside `updateListView(msg tea.KeyMsg)`, first check if `m.list.FilterState() == list.Filtering`.
2.  **If `true` (the user is typing a filter):**
    *   Pass the `msg` directly to `m.list, cmd = m.list.Update(msg)`.
    *   Return immediately. This ensures that all key presses are exclusively handled by the list component for filtering purposes.
3.  **If `false` (the list is not in active filtering mode):**
    *   Proceed with the existing `switch` statement to check for our custom application keybindings (`c`, `e`, `d`, `enter`, `q`).
    *   If a custom keybinding is matched, execute the corresponding action and return (to prevent the key press from being processed further).
    *   If no custom keybinding matches, fall through and pass the `msg` to `m.list, cmd = m.list.Update(msg)`. This allows the list to handle its own non-filtering keybindings, such as navigation (`j`, `k`, up/down arrows).

This change will correctly prioritize the filter input when it's active, while preserving the global keybindings when it's not, creating a more intuitive user experience.

## 3. Implementation Steps

0.  While researching the issue a matter came up the user also reported that the help menu does not
    show the custom keymaps add the keymaps to the help menu first.
1.  Create a new file `llm/plan_fix_tui_filter_keys.md` with the content above.
2.  Modify `tui.go` to implement the logic described in the solution. The `updateListView` function will be the primary target of this change.
