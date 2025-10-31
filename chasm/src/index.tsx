import { render, useKeyboard } from "@opentui/react";
import { StatusView } from "./StatusView.tsx";
import { DiffView } from "./DiffView.tsx";
import { updateData } from "./utils.ts";
import { COMMANDS, type Command, runCommand } from "./subcommand.ts";
import { useState, useEffect } from "react";
import type { DiffMap } from "./diff.ts";
import { type StatusGroups } from "./status.ts";

function App() {
  const [showCommand, setShowCommand] = useState(false);
  const [commandInput, setCommandInput] = useState("");
  const [feedback, setFeedback] = useState("");
  const [suggestions, setSuggestions] = useState<Command[]>([]);
  const [mode, setMode] = useState<"command" | "message">("command");
  const [pendingCommand, setPendingCommand] = useState<Command | null>(null);
  const [data, setData] = useState<{
    diffMap: DiffMap;
    statusGroups: StatusGroups;
  } | null>(null);

  useEffect(() => {
    (async () => {
      const d = await updateData();
      setData(d);
    })();
  }, []);

  async function executeCommand(cmd: Command | null, input: string) {
    if (mode === "message" && pendingCommand) {
      const msg = input.trim();
      if (!msg) {
        setFeedback("Message required");
        return;
      }
      try {
        if (pendingCommand.title === "Commit") {
          await runCommand("git", "commit", "-m", msg);
        } else if (pendingCommand.title === "Amend") {
          await runCommand("git", "commit", "--amend", "-m", msg);
        }
        setFeedback(`${pendingCommand.title} executed`);
        const d = await updateData();
        setData(d);
        setMode("command");
        setPendingCommand(null);
        setShowCommand(false);
        setCommandInput("");
      } catch (e: any) {
        setFeedback("Error: " + e.message);
      }
      return;
    }

    try {
      if (cmd) {
        if (cmd.title === "Commit" || cmd.title === "Amend") {
          setMode("message");
          setPendingCommand(cmd);
          setFeedback(`Enter ${cmd.title.toLowerCase()} message:`);
          setCommandInput("");
          return;
        } else {
          await runCommand(cmd.title, ...cmd.args);
          setFeedback(`${cmd.title} executed`);
          const d = await updateData();
          setData(d);
          setShowCommand(false);
          setCommandInput("");
        }
      } else {
        const parts = input.split(/\s+/);
        const command = parts[0];
        if (command === "add") {
          const files = parts.slice(1).join(" ") || ".";
          await runCommand("git", "add", files);
          setFeedback("Added successfully");
          const d = await updateData();
          setData(d);
          setShowCommand(false);
          setCommandInput("");
        } else {
          setFeedback("Unknown command");
        }
      }
    } catch (e: any) {
      setFeedback("Error: " + e.message);
    }
  }

  useEffect(() => {
    if (!showCommand || mode !== "command") return;
    const filtered = COMMANDS.filter(
      (c) =>
        c.title.toLowerCase().includes(commandInput.toLowerCase()) ||
        c.aliases.some((a) =>
          a.toLowerCase().includes(commandInput.toLowerCase()),
        ),
    );
    setSuggestions(filtered);
  }, [commandInput, showCommand, mode]);

  useKeyboard(async (key) => {
    if (key.name === "r") {
      const d = await updateData();
      setData(d);
      setFeedback("");
      return;
    }

    if (key.name === "p" && key.ctrl) {
      const newShow = !showCommand;
      setShowCommand(newShow);
      if (newShow) {
        setCommandInput("");
        setFeedback("");
        setMode("command");
        setPendingCommand(null);
      }
      return;
    }

    if (key.name === "q") {
      process.exit(0);
    }
  });

  return (
    <>
      {/* center that thing */}
      {/* two thirds of the screen height */}
      {showCommand && (
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
            focused={showCommand}
            value={commandInput}
            onInput={(e) => setCommandInput(e)}
            onSubmit={() => {
              executeCommand(suggestions[0] || null, commandInput);
            }}
          />
          <box />
          {mode === "command" &&
            suggestions
              .slice(0, 5)
              .map((cmd, i) => <text key={i}>{cmd.title}</text>)}
        </box>
      )}
      {feedback && <text>{feedback}</text>}
      <box border>
        {/* <scrollbox style={{ backgroundColor: "black", zIndex: 20 }} flexGrow={1}> */}
        {/*   <text> */}
        {/*     {JSON.stringify(parseGitStatus(status), null, 2)}{" "} */}
        {/*     {JSON.stringify(data?.statusGroups, null, 2)}{" "} */}
        {/*   </text> */}
        {/* </scrollbox> */}
        {data && (
          <box flexDirection="row" marginTop={1}>
            <StatusView statusGroups={data.statusGroups} />
            <DiffView diffMap={data.diffMap} />
          </box>
        )}
      </box>
    </>
  );
}

render(<App />);
