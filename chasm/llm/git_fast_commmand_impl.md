# Plan: Implement `git:fast` Command

The goal is to implement the `git:fast` command, which should stage all files, commit them with a user-provided message, and push the changes.

## 1. Understand `runCommand` and `ShellCommand` structure

First, I will read `src/subcommand.ts` to understand how `runCommand` is implemented and how the `SHELL_COMMANDS` are structured. This is crucial because the provided snippet for the `git:fast` command seems syntactically incorrect for a simple command executor. I need to know if `runCommand` handles command chaining (`&&`) and how it incorporates user input.

## 2. Modify `subcommand.ts`

Based on my findings from step 1, I will likely need to correct the `git:fast` command definition in `src/subcommand.ts`. A correct implementation would need to execute three commands in sequence. I might need to adjust `runCommand` if it doesn't support this, or format the `git:fast` command object in a way that `runCommand` understands.

For example, if `runCommand` can execute a shell script, the command might look like:
`"git add --all && git commit -m "${input}" && git push"`
I need to figure out how the `input` is substituted.

## 3. Modify `CommandPalette.tsx`

This component needs to be updated to handle the `git:fast` command.

### 3.1. Trigger Commit Message Input

Similar to `git:commit`, the `git:fast` command requires a commit message. I will update the `executeCommand` function in `CommandPalette.tsx` to recognize `git:fast` and open the message input dialog.

```diff
--- a/src/CommandPalette.tsx
+++ b/src/CommandPalette.tsx
@@ -173,7 +173,7 @@
       })();
       return;
     }
-if (cmd.title === "git:commit" || cmd.title === "git:amend") {
+if (cmd.title === "git:commit" || cmd.title === "git:amend" || cmd.title === "git:fast") {
       setPendingCommand(cmd);
       setShowMessage(true);
       setInput("");
```

### 3.2. Execution

The existing `onSubmit` logic for the message dialog should be sufficient to trigger the command. It calls `runCommand` with the `pendingCommand` and the entered message. No changes should be needed here, assuming `runCommand` and the `ShellCommand` definition are correctly implemented in `subcommand.ts`.

## 4. Verification

I will test the implementation by running the `git:fast` command from the command palette, entering a commit message, and verifying that `git status` shows a clean working tree and `git log` shows the new commit, and that the commit has been pushed.

This plan ensures that the new command is integrated correctly, reusing existing UI components and logic, while also addressing the likely issues in the underlying command definition.
