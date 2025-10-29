import type { KairosConfig, TimewCommand, CommandResult } from "./types.js";

export async function loadConfig(): Promise<KairosConfig> {
  const configPath = `${process.env.HOME}/.config/kairos/kairosv2.json`;
  const file = Bun.file(configPath);
  const exists = await file.exists();
  if (!exists) {
    Bun.write(file, "{}", { createPath: true });
  }
  const content = await file.text();
  return JSON.parse(content) as KairosConfig;
}

export async function composeAndExecuteSshCommand(
  command: TimewCommand,
  isDryRun: boolean,
): Promise<CommandResult> {
  const config = await loadConfig();
  let args: string[] = ["timew"];

  switch (command.type) {
    case "start":
      args.push("start");
      if (command.args.startTime) args.push(command.args.startTime);
      args.push(command.args.tag);
      break;
    case "stop":
      args.push("stop");
      if (command.args?.stopTime) args.push(command.args.stopTime);
      break;
    case "summary":
      args.push("summary");
      break;
    case "track":
      args.push(
        "track",
        command.args.start,
        command.args.end,
        command.args.tag,
      );
      break;
    case "inspect":
      // No additional args for inspect
      break;
    case "modify":
      args.push("modify", "@" + command.args.id);
      if (command.args.tag) args.push(command.args.tag);
      if (command.args.start) args.push(command.args.start);
      if (command.args.end) args.push(command.args.end);
      break;
    default:
      throw new Error(`Unknown command type: ${(command as any).type}`);
  }

  const sshArgs = ["ssh", `${config.user}@${config.host}`, ...args];

  if (isDryRun) {
    const cmdStr = sshArgs.join(" ");
    console.log(`Dry run: ${cmdStr}`);
    return { success: true, output: cmdStr };
  } else {
    try {
      const proc = Bun.spawn(sshArgs, { stdout: "pipe", stderr: "pipe" });
      const output = await new Response(proc.stdout).text();
      const error = await new Response(proc.stderr).text();
      const success = proc.exitCode === 0;
      const combinedOutput = `${output.trim()}${error.trim() ? '\n' + error.trim() : ''}`.trim();
      return { success, output: combinedOutput };
    } catch (err: unknown) {
      return { success: false, output: `Error: ${(err as Error).message}` };
    }
  }
}
