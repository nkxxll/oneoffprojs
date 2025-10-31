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

  async function executeCommand(cmd: Command, input: string) {
    try {
      if (cmd) {
        if (cmd.title === "Add All") {
          await runCommand(cmd.command, ...cmd.args);
        } else if (cmd.title === "Add File") {
          const msg = input.split(" ").slice(1).join(" ");
          if (!msg) {
            setFeedback("Add File require <file>");
            return;
          }
        } else if (cmd.title === "Commit") {
          const msg = input.split(" ").slice(1).join(" ");
          if (!msg) {
            setFeedback("Commit requires a message");
            return;
          }
          await runCommand("git", "commit", "-m", msg);
        } else if (cmd.title === "Amend") {
          const msg = input.split(" ").slice(1).join(" ");
          if (!msg) {
            setFeedback("Amend requires a message");
            return;
          }
          await runCommand("git", "commit", "--amend", "-m", msg);
        } else {
          await runCommand(cmd.command, ...cmd.args);
        }
        setFeedback(`${cmd.title} executed`);
        const d = await updateData();
        setData(d);
      } else {
        const parts = input.split(/\s+/);
        const command = parts[0];
        if (command === "add") {
          const files = parts.slice(1).join(" ") || ".";
          await runCommand("git", "add", files);
          setFeedback("Added successfully");
          const d = await updateData();
          setData(d);
        } else {
          setFeedback("Unknown command");
        }
      }
    } catch (e: any) {
      setFeedback("Error: " + e.message);
    }
  }

  useEffect(() => {
    if (!showCommand) return;
    const filtered = COMMANDS.filter(
      (c) =>
        c.title.toLowerCase().includes(commandInput.toLowerCase()) ||
        c.aliases.some((a) =>
          a.toLowerCase().includes(commandInput.toLowerCase()),
        ),
    );
    setSuggestions(filtered);
  }, [commandInput, showCommand]);

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
              if (suggestions[0]) {
                executeCommand(suggestions[0], commandInput);
              }
            }}
          />
          <box />
          {suggestions.slice(0, 5).map((cmd, i) => (
            <text key={i}>{cmd.title}</text>
          ))}
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
