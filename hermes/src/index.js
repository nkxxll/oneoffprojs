#!/usr/bin/env bun

// Main CLI entry point for Hermes

import { parseArgs } from './args.js';
import { loadConfig, processConfig } from './config.js';
import { runTests } from './runner.js';

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
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

  const configPath = args.configFile;
  if (!configPath) {
    console.error('Error: Config file path required');
    process.exit(1);
  }

  try {
    const config = await loadConfig(configPath);
    const processedConfig = processConfig(config);
    await runTests(processedConfig, args);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
