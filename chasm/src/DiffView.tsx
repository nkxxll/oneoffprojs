import { TextAttributes, type Color } from "@opentui/core";
import { type DiffMap, type DiffFile } from "./diff.ts";
import { useState } from "react";

interface DiffViewProps {
  diffMap: DiffMap;
}

export function DiffView({ diffMap }: DiffViewProps) {
  const [folds, setFolds] = useState<Map<number, boolean>>(() => {
    const initial = new Map<number, boolean>();
    diffMap.files.forEach((file, index) => {
      // Fold new, deleted, or mode-changed files; unfold others
      initial.set(index, file.isNew || file.isDeleted || file.hasModeChange);
    });
    return initial;
  });

  const toggleFold = (index: number) => {
    setFolds((prev) => new Map(prev).set(index, !prev.get(index)));
  };

  const getFileTitle = (file: DiffFile): { text: string; color: Color } => {
    if (file.isNew) return { text: `CREATED: ${file.to}`, color: "green" };
    if (file.isDeleted) return { text: `DELETED: ${file.from}`, color: "red" };
    if (file.hasModeChange)
      return {
        text: `MODE CHANGED: ${file.to} (${file.modeChange})`,
        color: "yellow",
      };
    const from = file.from.slice(2);
    const to = file.from.slice(2);
    return {
      text:
        from === to
          ? `MODIFIED: ${from}`
          : `RENAMED: ${file.from} -> ${file.to}`,
      color: "blue",
    };
  };

  return (
    <scrollbox flexGrow={1} marginLeft={2}>
      {diffMap.files.map((file, fileIndex) => {
        const { text: title, color } = getFileTitle(file);
        const isFolded = folds.get(fileIndex);
        return (
          <box key={fileIndex} flexDirection="column">
            {/* Vertical line separator (using a thin border) */}
            <text
              style={{ fg: color }}
              attributes={TextAttributes.BOLD}
              onMouseDown={() => toggleFold(fileIndex)}
            >
              {title} {isFolded ? "[+]" : "[-]"}{" "}
            </text>
            {!isFolded && (
              <box flexDirection="column" marginLeft={2}>
                {file.hunks.map((hunk, hunkIndex) => (
                  <box key={hunkIndex} flexDirection="column" marginTop={1}>
                    {/* <text attributes={TextAttributes.DIM}>{hunk.header}</text> */}
                    {hunk.lines.map((line, lineIndex) => {
                      let lineColor;
                      if (line.kind === "added") lineColor = "green";
                      else if (line.kind === "removed") lineColor = "red";
                      return (
                        <>
                          {lineColor ? (
                            <text key={lineIndex} style={{ fg: lineColor }}>
                              {line.content}
                            </text>
                          ) : (
                            <text
                              key={lineIndex}
                              attributes={TextAttributes.DIM}
                            >
                              {line.content}
                            </text>
                          )}
                        </>
                      );
                    })}
                  </box>
                ))}
              </box>
            )}
          </box>
        );
      })}
    </scrollbox>
  );
}
