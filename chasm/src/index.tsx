import { render, useKeyboard } from "@opentui/react";
import { StatusView } from "./StatusView.tsx";
import { DiffView } from "./DiffView.tsx";
import { updateData, getGitRoot } from "./utils.ts";
import { COMMANDS, type Command, runCommand } from "./subcommand.ts";
import { useState, useEffect } from "react";
import type { DiffMap } from "./diff.ts";
import { type StatusGroups } from "./status.ts";
import { Toast } from "./Toast.tsx";
import { Debugger } from "./Debugger.tsx";
import { CommandPalette } from "./CommandPalette.tsx";

function App() {
  const [showCommand, setShowCommand] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [gitRoot, setGitRoot] = useState<string>("");
  const [data, setData] = useState<{
    diffMap: DiffMap;
    statusGroups: StatusGroups;
  } | null>(null);

  useEffect(() => {
    (async () => {
      const root = await getGitRoot();
      setGitRoot(root);
      const d = await updateData();
      setData(d);
    })();
  }, []);

  useKeyboard(async (key) => {
    if (key.name === "r") {
      const d = await updateData();
      setData(d);
      setFeedback("");
      return;
    }

    if (key.name === "escape" || (key.name === "[" && key.ctrl)) {
      setShowCommand(false);
    }
    if (key.name === "p" && key.ctrl) {
      setShowCommand((show: boolean) => {
        setFeedback("");
        return true;
      });
      return;
    }

    if (key.name === "q") {
      process.exit(0);
    }
  });

  return (
    <>
      <Debugger debugging={false} status={""} data={{}} />
      <Toast
        message={feedback}
        duration={3000}
        onClose={() => setFeedback("")}
      />
      <CommandPalette
        show={showCommand}
        setFeedback={setFeedback}
        onUpdate={async () => {
          const d = await updateData();
          setData(d);
        }}
        cwd={gitRoot}
      />
      {data && (
        <box flexDirection="row">
          <StatusView statusGroups={data.statusGroups} />
          <DiffView diffMap={data.diffMap} />
        </box>
      )}
    </>
  );
}

render(<App />);
