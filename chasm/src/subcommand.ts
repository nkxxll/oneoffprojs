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
}

export interface ShellCommand {
  title: string;
  command: string[];
  input: boolean;
}

export const SHELL_COMMANDS: ShellCommand[] = [
  { title: "git:add", command: ["git", "add"], input: true },
  { title: "git:add-all", command: ["git", "add", "--all"], input: false },
  { title: "git:commit", command: ["git", "commit"], input: true },
  { title: "git:amend", command: ["git", "commit", "--amend"], input: true },
  { title: "git:push", command: ["git", "push"], input: false },
  {
    title: "git:push-force",
    command: ["git", "push", "--force"],
    input: false,
  },

  { title: "git:pull", command: ["git", "pull"], input: false },
  { title: "git:fetch", command: ["git", "fetch"], input: false },

  { title: "git:checkout", command: ["git", "checkout"], input: true },
  { title: "git:branch", command: ["git", "branch"], input: true },
  { title: "git:merge", command: ["git", "merge"], input: true },
  { title: "git:rebase", command: ["git", "rebase"], input: true },

  { title: "git:reset", command: ["git", "reset"], input: true },
  { title: "git:stash", command: ["git", "stash", "push"], input: false },
  { title: "git:stash-pop", command: ["git", "stash", "pop"], input: false },

  {
    title: "git:log",
    command: ["git", "log", "--oneline", "--graph", "--decorate"],
    input: false,
  },
];

export const COMMANDS: Command[] = [
  { title: "git:add", aliases: ["add", "stage"] },
  { title: "git:add-all", aliases: ["addall", "stageall", "aa"] },
  { title: "git:commit", aliases: ["commit", "cm"] },
  { title: "git:amend", aliases: ["amend", "fixcommit"] },
  { title: "git:push", aliases: ["push", "upload"] },
  { title: "git:push-force", aliases: ["forcepush", "pushf", "pf"] },

  { title: "git:pull", aliases: ["pull", "update", "sync"] },
  { title: "git:fetch", aliases: ["fetch", "get"] },

  { title: "git:checkout", aliases: ["co", "switch", "restore"] },
  { title: "git:branch", aliases: ["br", "newbranch", "branches"] },
  { title: "git:merge", aliases: ["merge", "combine", "join"] },
  { title: "git:rebase", aliases: ["rb", "reapply", "rebase"] },

  { title: "git:reset", aliases: ["undo", "uncommit", "resethead"] },
  { title: "git:stash", aliases: ["stash", "save", "stashsave"] },
  { title: "git:stash-pop", aliases: ["unstash", "applystash"] },

  { title: "git:status", aliases: ["status", "st", "info"] },
  { title: "git:diff", aliases: ["diff", "df", "compare"] },
  { title: "git:log", aliases: ["log", "history", "commits"] },
];

export async function runCommand(
  shellCmd: ShellCommand,
  userInput?: string,
): Promise<string> {
  let args: string[];
  switch (shellCmd.title) {
    case "git:add":
      args = ["git", "add", userInput || "."];
      break;
    case "git:commit":
      if (!userInput) throw new Error("Commit message required");
      args = ["git", "commit", "-m", userInput];
      break;
    case "git:amend":
      if (!userInput) throw new Error("Amend message required");
      args = ["git", "commit", "--amend", "-m", userInput];
      break;
    default:
      args = [...shellCmd.command];
      if (shellCmd.input) {
        if (!userInput) throw new Error("Input required for " + shellCmd.title);
        args.push(userInput);
      }
      break;
  }

  const proc = Bun.spawn(args, {
    stdout: "pipe",
    stderr: "pipe",
  });

  const output = await new Response(proc.stdout).text();
  const exitCode = await proc.exited;

  if (exitCode !== 0) {
    const error = await new Response(proc.stderr).text();
    throw new Error(`${shellCmd.title} failed: ${error}`);
  }

  return output;
}
