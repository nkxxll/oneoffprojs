import { useState, useEffect } from "react";
import {
  COMMANDS,
  SHELL_COMMANDS,
  type Command,
  type ShellCommand,
  runCommand,
} from "./subcommand";

export interface CommandPaletteProps {
  show: boolean;
  setFeedback: (feedback: string) => void;
}

export function CommandPalette({ show, setFeedback }: CommandPaletteProps) {
  const [input, setInput] = useState("");
  const [message, setMessage] = useState("");
  const [showMessage, setShowMessage] = useState(false);
  const [suggestions, setSuggestions] = useState<Command[]>([]);
  const [pendingCommand, setPendingCommand] = useState<Command | null>(null);

  useEffect(() => {
    if (!input) {
      setSuggestions([]);
      return;
    }
    const filtered = COMMANDS.filter(
      (c) =>
        c.title.toLowerCase().includes(input.toLowerCase()) ||
        c.aliases.some((a) => a.toLowerCase().includes(input.toLowerCase())),
    );
    setSuggestions(filtered);
  }, [input]);

  async function executeCommand(cmd: Command | null) {
    if (!cmd) {
      setFeedback("No command selected");
      return;
    }
    const shellCommand: ShellCommand | undefined = SHELL_COMMANDS.find(
      (command) => command.title === cmd.title,
    );
    if (!shellCommand) {
      setFeedback("Command not found");
      return;
    }
    if (cmd.title === "git:commit" || cmd.title === "git:amend") {
      setPendingCommand(cmd);
      setShowMessage(true);
      setInput("");
      setFeedback(`Enter ${cmd.title.split(":")[1]} message:`);
      return;
    }
    try {
      let userInput: string | undefined;
      if (shellCommand.input) {
        // Parse userInput from input, e.g., for "add file.txt", remove "add "
        const cmdName = cmd.title.split(":")[1];
        userInput =
          input.replace(new RegExp(`^${cmdName}\\s*`), "").trim() || undefined;
      }
      await runCommand(shellCommand, userInput);
      setFeedback(`${cmd.title} executed`);
      setInput("");
      setShowMessage(false);
    } catch (e: any) {
      setFeedback("Error: " + e.message);
    }
  }

  return (
    <>
      {showMessage && (
        <box
          border
          borderStyle="rounded"
          style={{
            position: "absolute",
            zIndex: 20,
            backgroundColor: "black",
            top: 2,
            left: "33%",
            width: "33%",
          }}
        >
          <text>Enter {pendingCommand?.title.split(":")[1]} message:</text>
          <input
            focused={showMessage}
            value={message}
            style={{ height: 1 }}
            onInput={(e) => setMessage(e)}
            onSubmit={async () => {
              if (!pendingCommand) return;
              const shellCommand = SHELL_COMMANDS.find(
                (c) => c.title === pendingCommand.title,
              );
              if (!shellCommand) return;
              try {
                await runCommand(shellCommand, message);
                setFeedback(`${pendingCommand.title} executed`);
                setMessage("");
                setPendingCommand(null);
                setShowMessage(false);
                setInput("");
              } catch (e: any) {
                setFeedback("Error: " + e.message);
              }
            }}
          />
          <box />
        </box>
      )}
      {show && !showMessage && (
        <box
          border
          borderStyle="rounded"
          style={{
            position: "absolute",
            zIndex: 20,
            backgroundColor: "black",
            top: 2,
            left: "33%",
            width: "33%",
          }}
        >
          <input
            focused={show}
            value={input}
            style={{ height: 1 }}
            onInput={(e) => setInput(e)}
            onSubmit={() => {
              executeCommand(suggestions[0] || null);
            }}
          />
          <box />
          {input &&
            suggestions
              .slice(0, 5)
              .map((cmd, i) => <text key={i}>{cmd.title}</text>)}
        </box>
      )}
    </>
  );
}
