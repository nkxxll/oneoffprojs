import { render, useKeyboard } from "@opentui/react";
import { StatusView } from "./StatusView.tsx";
import { DiffView } from "./DiffView.tsx";
import { updateData } from "./utils.ts";
import { useState, useEffect } from "react";
import type { DiffMap } from "./parse.ts";
import type { StatusGroups } from "./status.ts";

function App() {
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

  useKeyboard(async (key) => {
    if (key.code === "r" && key.shift) {
      const d = await updateData();
      setData(d);
      return;
    }
  });

  return (
    <box border>
      {data && (
        <box flexDirection="row" marginTop={1}>
          <StatusView statusGroups={data.statusGroups} />
          <DiffView diffMap={data.diffMap} />
        </box>
      )}
    </box>
  );
}

render(<App />);
