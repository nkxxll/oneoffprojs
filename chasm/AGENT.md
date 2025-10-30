# This is the docu for the Agent

This is a text user interface that interactively shows the user the git status and git diff.
The main concern is that the information should be visible on the first look the ui should be
compact.
The user interactions should be either done by mouse or by keyboard.

## Commands

- run tests `bun test`

### DONT RUN THESE

- don't run `bun run dev` this is an interactive terminal application

## Architecture

- `src/index.tsx` all tui components and the entry point of the tui
- `src/parse.ts` git diff parser
