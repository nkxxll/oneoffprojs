# Prompt Manager

Predefined prompts are the future of agentic work! **Prompt manager** is an tui application that
works with Tmux to stream saved prompts into a coding agent.

## Gif

![demo tape](./assets/prompt-manager-demo.gif)

## Motivation

I did write something similar for the web but it does not work because the ux is too bad I type
faster than opening the web app. Prompt manager lets you write prompts with placeholders and fill
them on the fly. They will be streamed into the Tmux terminal buffer with a coding agent. PM also
lets you manage your prompts CRUD in a file that can be synced with version control.

Important Questions:

- Is this an overkill could you just use a shell script like my PoC that I used before? Yes
- Can `gemini` write this in one to two days of work? Yes
- Will I do this because I can? Yes

## Requirements

- [x] cli interface

  ```
  Usage:
    prompt-manager [flags]
    prompt-manager [command]

  Available Commands:
    completion  Generate the autocompletion script for the specified shell
    create      Create a new prompt
    help        Help about any command
    list        List all prompts
    remove      Remove a prompt
    search      Search for prompts by name or tag
    update      Update an existing prompt

  Flags:
    -h, --help            help for prompt-manager
    -t, --target string   tmux target pane (e.g., session:window.pane)
  ```

- [x] write a tui to do the same things interactively

## Sturcture

- `main.go` entry point
- `cli.go` cli argument parsing and logic
- `tui.go` bubble tea code that defines the tui
- `storage.go` manages the prompt file
- `tmux.go` calls the Tmux application handles possible errors with the call
- `fzf.go` calls the fzf application so you can choose a prompt.
- `promptparser.go` parses templated prompts
