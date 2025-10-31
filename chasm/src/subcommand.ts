export async function getGitDiff(): Promise<string> {
  const proc = Bun.spawn(["git", "diff"], {
    stdout: "pipe",
    stderr: "pipe",
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`git diff failed: ${error}`);
  }

  return output;
}

export async function getGitStatus(): Promise<string> {
  const proc = Bun.spawn(["git", "status", "--porcelain"], {
    stdout: "pipe",
    stderr: "pipe",
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`git status failed: ${error}`);
  }

  return output;
}

export interface Command {
  title: string;
  aliases: string[];
  command: string;
  args: string[];
}

export const COMMANDS: Command[] = [
  { title: "Push", aliases: ["Puhs", "Psuh"], command: "git", args: ["push"] },
  {
    title: "Push Force",
    aliases: ["Force"],
    command: "git",
    args: ["push", "-f"],
  },
  {
    title: "Push (Dial)",
    aliases: ["Push Dialogue", "PDial"],
    command: "git",
    args: ["push"],
  },
  { title: "Commit", aliases: [], command: "git", args: ["commit"] },
  { title: "Add All", aliases: ["all"], command: "git", args: ["add", "-A"] },
  {
    title: "Add File",
    aliases: ["afile", "addf"],
    command: "git",
    args: ["add"],
  },
  { title: "Amend", aliases: [], command: "git", args: ["commit", "--amend"] },
  {
    title: "Amend (no edit)",
    aliases: ["No Edit", "AMEND"],
    command: "git",
    args: ["commit", "--amend", "--no-edit"],
  },
];

async function runCommandImpl(
  command: string,
  args: string[],
): Promise<string> {
  const proc = Bun.spawn([command, ...args], {
    stdout: "pipe",
    stderr: "pipe",
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`${command} ${args.join(" ")} failed: ${error}`);
  }

  return output;
}

export async function runCommand(
  command: string,
  ...args: string[]
): Promise<string> {
  return runCommandImpl(command, args);
}
