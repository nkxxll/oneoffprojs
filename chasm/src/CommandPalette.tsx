import { useState, useEffect } from "react";
import { useKeyboard } from "@opentui/react";
import {
  COMMANDS,
  SHELL_COMMANDS,
  type Command,
  type ShellCommand,
  runCommand,
  getGitStatus,
} from "./subcommand";
import { fuzzySearch } from "./fuzzy";

export type ScoredCommand = Command & { score: number };

export interface CommandPaletteProps {
  show: boolean;
  setFeedback: (feedback: string) => void;
  onUpdate: () => Promise<void>;
  cwd: string;
}

export function CommandPalette({
  show,
  setFeedback,
  onUpdate,
  cwd,
}: CommandPaletteProps) {
  const [input, setInput] = useState("");
  const [message, setMessage] = useState("");
  const [showMessage, setShowMessage] = useState(false);
  const [suggestions, setSuggestions] = useState<ScoredCommand[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [pendingCommand, setPendingCommand] = useState<Command | null>(null);
  const [showFileSelector, setShowFileSelector] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const [fileIndex, setFileIndex] = useState(0);

  useEffect(() => {
    if (!input) {
      setSuggestions([]);
      setSelectedIndex(0);
      return;
    }
    const results = fuzzySearch(input, COMMANDS);
    setSuggestions(results);
    setSelectedIndex(0);
  }, [input]);

  useKeyboard(async (key) => {
    if (!show) return;
    if (showFileSelector) {
      if (key.name === "up" || key.name === "k") {
        setFileIndex((prev) => Math.max(0, prev - 1));
        return;
      }
      if (key.name === "down" || key.name === "j") {
        setFileIndex((prev) => Math.min(files.length - 1, prev + 1));
        return;
      }
      if (key.name === "space") {
        setSelectedFiles((prev) => {
          const newSet = new Set(prev);
          const file = files[fileIndex]!;
          if (newSet.has(file)) {
            newSet.delete(file);
          } else {
            newSet.add(file);
          }
          return newSet;
        });
        return;
      }
      if (key.name === "return") {
        // Confirm selection
        const shellCommand = SHELL_COMMANDS.find((c) => c.title === "git:add");
        if (!shellCommand) return;
        try {
          const userInput = Array.from(selectedFiles);
          await runCommand(shellCommand, userInput, cwd);
          setFeedback("git:add executed");
          await onUpdate();
          setShowFileSelector(false);
          setInput("");
        } catch (e: any) {
          setFeedback("Error: " + e.message);
        }
        return;
      }
      if (key.name === "escape" || (key.name === "[" && key.ctrl)) {
        setShowFileSelector(false);
        // input captures the [ key as input
        setInput("");
        return;
      }
      return;
    }
    if (key.ctrl && key.name === "w") {
      setInput((inp: string) => {
        return inp.split(" ").slice(0, -1).join(" ") || "";
      });
      return;
    }
    if (key.ctrl && key.name === "p") {
      setSelectedIndex((prev) => Math.max(0, prev - 1));
      return;
    }
    if (key.ctrl && key.name === "n") {
      setSelectedIndex((prev) => Math.min(suggestions.length - 1, prev + 1));
      return;
    }
  });

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
    if (cmd.title === "git:add") {
      // Show file selector for unstaged files
      (async () => {
        try {
          const status = await getGitStatus();
          const lines = status
            .split("\n")
            .slice(1)
            .filter((line) => line.trim() && line[1] !== " ");
          const unstagedFiles = lines.map((line) => line.slice(3));
          setFiles(unstagedFiles);
          setSelectedFiles(new Set());
          setFileIndex(0);
          setShowFileSelector(true);
          setInput("");
        } catch (e: any) {
          setFeedback("Error getting git status: " + e.message);
        }
      })();
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
      runCommand(shellCommand, userInput, cwd).then(() => {
        setFeedback(`${cmd.title} executed`);
        onUpdate();
      });
      setInput("");
      setShowMessage(false);
    } catch (e: any) {
      setFeedback("Error: " + e.message);
    }
  }

  return (
    <>
      {showFileSelector && (
        <box
          border
          borderStyle="rounded"
          style={{
            position: "absolute",
            zIndex: 20,
            backgroundColor: "black",
            top: 2,
            left: "20%",
            width: "60%",
            height: "80%",
          }}
        >
          <text>
            Select files to stage (Space to toggle, Enter to confirm, Esc to
            cancel):
          </text>
          <box flexDirection="column" style={{ overflow: "hidden" }}>
            {files.slice(0, 20).map((file, i) => (
              <text
                key={i}
                style={i === fileIndex ? { bg: "blue" } : { bg: "black" }}
              >
                [{selectedFiles.has(file) ? "x" : " "}] {file}
              </text>
            ))}
          </box>
        </box>
      )}
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
                await runCommand(shellCommand, message, cwd);
                setFeedback(`${pendingCommand.title} executed`);
                await onUpdate();
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
      {show && !showMessage && !showFileSelector && (
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
              executeCommand(suggestions[selectedIndex] || null);
            }}
          />
          <box />
          {input &&
            suggestions.slice(0, 5).map((cmd, i) => (
              <text
                key={i}
                style={i === selectedIndex ? { bg: "blue" } : { bg: "black" }}
              >
                {cmd.title}
              </text>
            ))}
        </box>
      )}
    </>
  );
}
