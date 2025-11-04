import { TextAttributes, type Color } from "@opentui/core";
import { type DiffMap, type DiffFile } from "./diff.ts";
import { useState } from "react";
import {
  COLOR9 as RED,
  COLOR10 as GREEN,
  COLOR11 as YELLOW,
  COLOR4 as BLUE,
} from "./themes.ts";

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
    if (file.isNew) return { text: `CREATED: ${file.to}`, color: GREEN };
    if (file.isDeleted) return { text: `DELETED: ${file.from}`, color: RED };
    if (file.hasModeChange)
      return {
        text: `MODE CHANGED: ${file.to} (${file.modeChange})`,
        color: YELLOW,
      };
    const from = file.from.slice(2);
    const to = file.from.slice(2);
    return {
      text:
        from === to
          ? `MODIFIED: ${from}`
          : `RENAMED: ${file.from} -> ${file.to}`,
      color: BLUE,
    };
  };

  return (
    <scrollbox border borderStyle="rounded" flexGrow={1} marginLeft={2}>
      {diffMap.files.map((file, fileIndex) => {
        const { text: title, color } = getFileTitle(file);
        const isFolded = folds.get(fileIndex);
        return (
          <box key={fileIndex} flexDirection="column">
            {/* Vertical line separator (using a thin border) */}
            <box onMouseDown={() => toggleFold(fileIndex)}>
              <text
                style={{ fg: color }}
                attributes={TextAttributes.BOLD}
                selectable={false}
              >
                {title} {isFolded ? "[+]" : "[-]"}{" "}
              </text>
            </box>
            {!isFolded && (
              <box flexDirection="column" marginLeft={2}>
                {file.hunks.map((hunk, hunkIndex) => (
                  <box
                    key={`${fileIndex}-${hunkIndex}`}
                    flexDirection="column"
                    marginTop={1}
                  >
                    {/* <text attributes={TextAttributes.DIM}>{hunk.header}</text> */}
                    {hunk.lines.map((line, lineIndex) => {
                      let lineColor;
                      if (line.kind === "added") lineColor = GREEN;
                      else if (line.kind === "removed") lineColor = RED;
                      return (
                        <text
                          key={`${fileIndex}-${hunkIndex}-${lineIndex}`}
                          style={lineColor ? { fg: lineColor } : undefined}
                          attributes={
                            lineColor ? undefined : TextAttributes.DIM
                          }
                        >
                          {line.content}
                        </text>
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
