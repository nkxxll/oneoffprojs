# Prompt Manager

Predefined prompts are the future of agentic work! **Prompt manager** is an tui application that
works with Tmux to stream saved prompts into a coding agent.

## Motivation

I did write something similar for the web but it does not work because the ux is too bad I type
faster than opening the web app. Prompt manager lets you write prompts with placeholders and fill
them on the fly. They will be streamed into the Tmux terminal buffer with a coding agent. PM also
lets you manage your prompts CRUD in a file that can be synced with version control.

Important Questions:

- Is this an overkill could you just use a shell script like my poc that I used before? Yes
- Can gemini write this in one to two days of work? Yes
- Will I do this because I can? Yes

## Requirements

- [ ] cli interface

  ```
  Usage: prompt-cli [command] [options]

  Manage your prompt collection from the terminal.

  Commands:
    create   Create a new prompt.
    remove   Delete a prompt by ID or name.
    update   Update an existing prompt.
    display  List all prompts or display a specific prompt.
    search   Search prompts by keyword or tag.
    help     Show this help message.

  Options:
    -n, --name <name>          Prompt name.
    -i, --id <id>              Prompt ID.
    -p, --prompt <text>        Prompt text.
    -t, --target <window id>   Tmux target window.
    -f, --force                Force deletion without confirmation.
    -v, --verbose              Show detailed output.
    -h, --help                 Display this help message.

  Examples:
    prompt-cli create -n "Summarize Article" -d "Summarizes articles" -t "summary,writing"
    prompt-cli update -i 42 -d "Updated description"
    prompt-cli display
    prompt-cli remove -i 42 -f
    prompt-cli -t @6
  ```

- [ ] write a tui to do the same things interactively

## Sturcture

- `promptcli.go` entry point
- `cli.go` cli argument parsing and logic
- `tui.go` bubble tea code that defines the tui
- `storage.go` manages the prompt file
- `tmux.go` calls the Tmux application handles possible errors with the call
- `fzf.go` calls the fzf application so you can choose a prompt.
