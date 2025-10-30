import { TextAttributes } from "@opentui/core";
import { DiffMap } from "./parse.ts";

interface DiffViewProps {
  diffMap: DiffMap;
}

export function DiffView({ diffMap }: DiffViewProps) {
  return (
    <box flexDirection="column" flexGrow={1} marginLeft={2}>
      {diffMap.files.map((file, fileIndex) => (
        <box key={fileIndex} flexDirection="column" marginBottom={2}>
          <text attributes={TextAttributes.BOLD}>
            diff --git {file.from} {file.to}
          </text>
          {file.hunks.map((hunk, hunkIndex) => (
            <box key={hunkIndex} flexDirection="column" marginTop={1}>
              <text attributes={TextAttributes.DIM}>{hunk.header}</text>
              {hunk.lines.map((line, lineIndex) => {
                let color = TextAttributes.DIM;
                if (line.kind === 'added') color = TextAttributes.GREEN;
                else if (line.kind === 'removed') color = TextAttributes.RED;
                return (
                  <text key={lineIndex} attributes={color}>
                    {line.content}
                  </text>
                );
              })}
            </box>
          ))}
        </box>
      ))}
    </box>
  );
}
