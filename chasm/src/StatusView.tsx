import { TextAttributes } from "@opentui/core";
import { type StatusGroups } from "./status.ts";

interface StatusViewProps {
  statusGroups: StatusGroups;
}

export function StatusView({ statusGroups }: StatusViewProps) {
  const { staged, unstaged, untracked } = statusGroups;

  const sections = [
    { title: "STAGED", files: staged, color: "green" },
    { title: "UNSTAGED", files: unstaged, color: "yellow" },
    { title: "UNTRACKED", files: untracked, color: "red" },
  ];

  return (
    <box flexDirection="column" width={40}>
      {sections.map(
        ({ title, files, color }) =>
          files.length > 0 && (
            <box key={title} flexDirection="column" marginBottom={1}>
              <text fg={color}>{title}:</text>
              {files.map((file, i) => (
                <text key={i} attributes={TextAttributes.DIM}>
                  {file.staged !== " " ? file.staged : file.unstaged}{" "}
                  {file.file}
                </text>
              ))}
            </box>
          ),
      )}
    </box>
  );
}
