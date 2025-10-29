#!/usr/bin/env bun

import { parseArgs } from "util";
import { loadConfig, processConfig } from "./config.js";
import { runTests } from "./runner.js";
import { displayResults } from "./output.js";

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv,
    options: {
      help: {
        type: "boolean",
        short: "h",
      },
      verbose: {
        type: "boolean",
        short: "v",
      },
      quiet: {
        type: "boolean",
        short: "q",
      },
    },
    strict: true,
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`Hermes - MCP Server Testing Tool

Usage: hermes [options] <config-file>

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -q, --quiet    Enable quiet mode

Examples:
  hermes config.toml
  hermes -v test-config.toml
`);
    process.exit(0);
  }

  if (positionals.length < 2) {
    console.log(`Hermes - MCP Server Testing Tool

Usage: hermes [options] <config-file>

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -q, --quiet    Enable quiet mode

Examples:
  hermes config.toml
  hermes -v test-config.toml
`);
    process.exit(1);
  }

  const configPath = positionals[positionals.length - 1]!;
  try {
    const config = await loadConfig(configPath);
    const processedConfig = processConfig(config);
    const results = await runTests(processedConfig, {
      help: values.help || false,
      verbose: values.verbose || false,
      quiet: values.quiet || false,
    });
    displayResults(results);
  } catch (error) {
    console.error(`Error: ${(error as Error).message}`);
    process.exit(1);
  }
}

main();
