import { TextAttributes } from "@opentui/core";
import { type StatusGroups } from "./status.ts";
import {
  COLOR10 as GREEN,
  COLOR11 as YELLOW,
  COLOR9 as RED,
  COLOR4 as BLUE,
} from "./themes.ts";

interface StatusViewProps {
  statusGroups: StatusGroups;
}

export function StatusView({ statusGroups }: StatusViewProps) {
  const { branch, staged, unstaged, untracked } = statusGroups;

  const sections = [
    { title: "STAGED", files: staged, color: GREEN },
    { title: "UNSTAGED", files: unstaged, color: YELLOW },
    { title: "UNTRACKED", files: untracked, color: RED },
  ];

  return (
    <box border borderStyle="rounded" flexDirection="column" width={40}>
      <box flexDirection="column" marginBottom={1}>
        <text fg={BLUE}>BRANCH: {branch.branch}</text>
        {branch.ahead > 0 && <text fg={GREEN}>AHEAD: {branch.ahead}</text>}
        {branch.behind > 0 && <text fg={RED}>BEHIND: {branch.behind}</text>}
      </box>
      {sections
        .filter(({ files }) => files.length > 0)
        .map(({ title, files, color }) => (
          <box key={title} flexDirection="column" marginBottom={1}>
            <text fg={color}>{title}:</text>
            {files.map((file, i) => (
              <text key={i} attributes={TextAttributes.DIM}>
                {file.staged !== " " ? file.staged : file.unstaged} {file.file}
              </text>
            ))}
          </box>
        ))}
    </box>
  );
}
