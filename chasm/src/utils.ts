import { parse as parseGitDiff } from "./diff";
import { getGitDiff, getGitStatus, runCommand } from "./subcommand";
import { parseGitStatus, groupStatusFiles } from "./status";

export async function updateData() {
  const [diff, status] = await Promise.all([getGitDiff(), getGitStatus()]);
  const diffMap = parseGitDiff(diff);
  const { branchInfo, statusFiles } = parseGitStatus(status);
  const statusGroups = groupStatusFiles({ branchInfo, statusFiles });
  return { diffMap, statusGroups };
}

export { runCommand };

export type Color = "green" | "yellow" | "white" | "blue" | "red";
