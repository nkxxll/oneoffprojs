import { parse as parseGitDiff } from "./diff";
import { getGitDiff, getGitStatus, runCommand, getGitRoot } from "./subcommand";
import { parseGitStatus, groupStatusFiles } from "./status";

export async function updateData() {
  const gitRoot = await getGitRoot();
  const [diff, status] = await Promise.all([getGitDiff(gitRoot), getGitStatus(gitRoot)]);
  const diffMap = parseGitDiff(diff);
  const { branchInfo, statusFiles } = parseGitStatus(status);
  const statusGroups = groupStatusFiles({ branchInfo, statusFiles });
  return { diffMap, statusGroups };
}

export { runCommand, getGitRoot };

export type Color = "green" | "yellow" | "white" | "blue" | "red";
