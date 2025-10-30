import { TextAttributes } from "@opentui/core";
import {
  getAllFileStatuses,
  type FileStatus,
  type DiffMap,
  type DiffFile,
} from "./parse.ts";

interface StatusComponentProps {
  diffMap: DiffMap;
}

export function StatusComponent({ diffMap }: StatusComponentProps) {
  const fileStatuses = getAllFileStatuses(diffMap);

  const grouped = fileStatuses.reduce(
    (acc, { file, status }) => {
      if (!acc[status]) acc[status] = [];
      acc[status].push(file);
      return acc;
    },
    {} as Record<FileStatus, DiffFile[]>,
  );

  const fgStyles = {
    added: "green",
    deleted: "red",
    renamed: "yellow",
    modified: "white",
  } as const;

  return (
    <box flexDirection="column">
      {(["added", "deleted", "modified", "renamed"] as FileStatus[]).map(
        (status) => {
          const files = grouped[status] || [];
          if (files.length === 0) return null;
          const style = { fg: fgStyles[status] };

          return (
            <box key={status} flexDirection="column" marginBottom={1}>
              <text style={style}>{status.toUpperCase()}:</text>
              {files.map((file, i) => (
                <text key={i} attributes={TextAttributes.DIM}>
                  {status === "renamed"
                    ? `${file.from} -> ${file.to}`
                    : file.to}
                </text>
              ))}
            </box>
          );
        },
      )}
    </box>
  );
}
