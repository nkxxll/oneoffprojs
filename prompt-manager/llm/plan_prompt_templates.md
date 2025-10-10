# Plan: Implement Prompt Templates

This document outlines the plan to add support for template fields in prompts.

## 1. Prompt Parser (`promptparser.go`)

A new file `promptparser.go` will be created to handle parsing and rendering of prompt templates.

### Functions:

- **`ParseTemplate(text string) []string`**:
  - This function will take a string (the prompt text) as input.
  - It will parse the string for template fields, which are expected to be in the format `{{field_name}}`.
  - It will return a slice of strings containing the names of the found template fields. If no fields are found, it will return an empty slice.

- **`RenderTemplate(text string, values map[string]string) string`**:
  - This function will take the prompt text and a map of field names to their values.
  - It will replace the template fields in the text with their corresponding values from the map.
  - It will return the rendered string.

## 2. TUI Enhancements (`tui.go`)

The TUI will be updated to handle prompts with template fields.

### State Management:

- A new view state, `templateView`, will be added to the `viewState` enum to represent the state where the user is filling in template fields.

### Model changes:

- The `tuiModel` struct will be extended to include a `templateForm` field, which will manage the state of the template-filling form.

- A new `TemplateForm` struct will be created:
  ```go
  type TemplateForm struct {
      inputs      []textinput.Model
      focusIndex  int
      promptText  string
  }
  ```
  - `inputs`: A slice of `textinput.Model` from the `bubbletea` library, one for each template field.
  - `focusIndex`: To keep track of the currently focused input field.
  - `promptText`: The original text of the prompt being processed.

### Workflow for selecting a prompt:

1.  When the user selects a prompt from the list (presses `Enter`):
2.  The application will call `promptparser.ParseTemplate()` with the prompt's text.
3.  **If no template fields are found:** The prompt text is sent to the `tmux` pane as is, and the application quits.
4.  **If template fields are found:**
    - The TUI state will switch to `templateView`.
    - A new `TemplateForm` will be created, dynamically generating a `textinput.Model` for each field identified by the parser.

### `templateView` Implementation:

- **`updateTemplateView(msg tea.Msg)`**:
  - This function will handle user input within the `templateView`.
  - It will manage focus switching between the different `textinput.Model`s (e.g., using `Tab` or `Enter`).
  - When the user confirms the input (e.g., by pressing `Enter` on the last field):
    1.  The values from all `textinput.Model`s are collected into a map.
    2.  `promptparser.RenderTemplate()` is called with the original prompt text and the map of values.
    3.  The resulting rendered prompt is sent to the `tmux` pane.
    4.  The application quits.
  - Pressing `Esc` will cancel the operation and return the user to the `listView`.

- **`TemplateForm.View()`**:
  - This method will render the form, displaying all the `textinput.Model`s for the user to fill in.

This approach ensures that the existing functionality is preserved for prompts without templates, while providing a dynamic and user-friendly way to handle prompts that require user input.
