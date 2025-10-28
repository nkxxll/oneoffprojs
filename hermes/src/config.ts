import { readFile } from "fs/promises";
import { parse } from "toml";
import type { Config, Message, ProcessedConfig, RawTest } from "./types";

export async function loadConfig(configPath: string): Promise<Config> {
  try {
    const content = await readFile(configPath, "utf-8");
    const config = parse(content);
    // Basic validation
    validateConfig(config);
    return config;
  } catch (error) {
    throw new Error(`Failed to load config: ${(error as Error).message}`);
  }
}

function validateConfig(config: any): void {
  if (!config.cmd) {
    throw new Error("Config must have cmd and args");
  }
  if (!config.test_runs || !Array.isArray(config.test_runs)) {
    throw new Error("Config must have test_runs array");
  }
  for (const run of config.test_runs) {
    if (!run.tests || !Array.isArray(run.tests)) {
      throw new Error("Each test_run must have tests array");
    }
    for (const test of run.tests) {
      if (!test.type) {
        throw new Error("Each test must have type");
      }
      if (test.type === "tools/call") {
        if (!test.params && (!test.tool || !test.args)) {
          throw new Error("tools/call test must have params or tool+args");
        }
      }
    }
  }
}

export function processConfig(config: Config): ProcessedConfig {
  let id = 1;
  const testRuns = config.test_runs.map((run) => ({
    name: run.name || "unnamed run",
    tests: run.tests.map((test) => ({
      ...test,
      message: generateMessage(test, id++),
    })),
  }));
  return {
    cmd: config.cmd,
    args: config.args,
    testRuns,
  };
}

function generateMessage(test: RawTest, id: number): Message {
  const base = { jsonrpc: "2.0" };
  switch (test.type) {
    case "initialize":
      return { ...base, id, method: "initialize", params: test.params || {} };
    case "notifications/initialized":
      return { ...base, method: "notifications/initialized" };
    case "list/tools":
      return { ...base, id, method: "tools/list" };
    case "tools/call":
      const params = test.params || {
        name: test.tool,
        arguments: test.args || [],
      };
      return { ...base, id, method: "tools/call", params };
    default:
      throw new Error(`Unknown test type: ${test.type}`);
  }
}
