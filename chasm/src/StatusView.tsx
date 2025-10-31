import { TextAttributes } from "@opentui/core";
import { type StatusGroups } from "./status.ts";

interface StatusViewProps {
  statusGroups: StatusGroups;
}

export function StatusView({ statusGroups }: StatusViewProps) {
  const { branch, staged, unstaged, untracked } = statusGroups;

  const sections = [
    { title: "STAGED", files: staged, color: "green" },
    { title: "UNSTAGED", files: unstaged, color: "yellow" },
    { title: "UNTRACKED", files: untracked, color: "red" },
  ];

  return (
    <box flexDirection="column" width={40}>
      <box flexDirection="column" marginBottom={1}>
        <text fg="blue">BRANCH: {branch.branch}</text>
        {branch.ahead > 0 && <text fg="green">AHEAD: {branch.ahead}</text>}
        {branch.behind > 0 && <text fg="red">BEHIND: {branch.behind}</text>}
      </box>
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
