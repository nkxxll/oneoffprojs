import { parse } from "./parse";
import { getGitDiff, getGitStatus } from "./subcommand";
import { parseGitStatus, groupStatusFiles } from "./status";

export async function updateData() {
  const [diff, status] = await Promise.all([getGitDiff(), getGitStatus()]);
  const diffMap = parse(diff);
  const statusFiles = parseGitStatus(status);
  const statusGroups = groupStatusFiles(statusFiles);
  return { diffMap, statusGroups };
}
