import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { composeAndExecuteSshCommand } from "./commandComposer.js";
import { parseArgs } from "util";

const { values, positionals: _positionals } = parseArgs({
  args: Bun.argv,
  options: {
    help: { type: "boolean", short: "h" },
    dry: { type: "boolean", short: "d" },
  },
  allowPositionals: true,
});

if (values.help) {
  console.log(`
Kairos v2 MCP Server

Usage: bun run index.ts [options]

Options:
  -h, --help    Show this help message
  -d, --dry     Run in dry mode (log commands without executing)

This server provides MCP tools for time tracking via SSH to a remote timew instance.
  `);
  process.exit(0);
}

const isDryRun = values.dry || false;

// Create an MCP server
const server = new McpServer({
  name: "kairosv2",
  version: "1.0.0",
});

// Register timew_start tool
server.registerTool(
  "timew_start",
  {
    title: "Start Time Tracking",
    description: "Start tracking time for a task",
    inputSchema: { tag: z.string(), startTime: z.string().optional() },
    outputSchema: { output: z.string(), success: z.boolean() },
  },
  async ({ tag, startTime }) => {
    const result = await composeAndExecuteSshCommand(
      { type: "start", args: { tag, startTime } },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else if (result.success) {
      message = `Command executed successfully: ${result.output}`;
    } else {
      message = `Command failed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: { success: result.success, output: result.output },
    };
  },
);

// Register timew_stop tool
server.registerTool(
  "timew_stop",
  {
    title: "Stop Time Tracking",
    description: "Stop the current time tracking",
    inputSchema: { stopTime: z.string().optional() },
    outputSchema: { output: z.string(), success: z.boolean() },
  },
  async ({ stopTime }) => {
    const result = await composeAndExecuteSshCommand(
      { type: "stop", args: stopTime ? { stopTime } : undefined },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else if (result.success) {
      message = `Command executed successfully: ${result.output}`;
    } else {
      message = `Command failed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: { success: result.success, output: result.output },
    };
  },
);

// Register timew_summary tool
server.registerTool(
  "timew_summary",
  {
    title: "Get Time Summary",
    description: "Get a summary of tracked time",
    inputSchema: {},
    outputSchema: { success: z.boolean(), output: z.string() },
  },
  async () => {
    const result = await composeAndExecuteSshCommand(
      { type: "summary" },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else if (result.success) {
      message = `Command executed successfully: ${result.output}`;
    } else {
      message = `Command failed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: { success: result.success, output: result.output },
    };
  },
);

// Register timew_inspect tool
server.registerTool(
  "timew_inspect",
  {
    title: "Inspect Current Time Tracking",
    description: "Show the current running time tracker",
    inputSchema: {},
    outputSchema: { output: z.string(), success: z.boolean() },
  },
  async () => {
    const result = await composeAndExecuteSshCommand(
      { type: "inspect" },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else {
      message = `Command executed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: {
        success: result.success || !!result.output.trim(),
        output: result.output,
      },
    };
  },
);

// Register timew_modify tool
server.registerTool(
  "timew_modify",
  {
    title: "Modify Tracked Time",
    description:
      "Modify the tag, start, or end time of an existing tracked interval",
    inputSchema: {
      id: z.string(),
      tag: z.string().optional(),
      start: z.string().optional(),
      end: z.string().optional(),
    },
    outputSchema: { output: z.string(), success: z.boolean() },
  },
  async ({ id, tag, start, end }) => {
    const result = await composeAndExecuteSshCommand(
      { type: "modify", args: { id, tag, start, end } },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else if (result.success) {
      message = `Command executed successfully: ${result.output}`;
    } else {
      message = `Command failed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: { success: result.success, output: result.output },
    };
  },
);

// Register timew_track tool
server.registerTool(
  "timew_track",
  {
    title: "Track Time for Period",
    description: "Track time for a specific period",
    inputSchema: {
      startISO: z.string().datetime({ offset: true }),
      endISO: z.string().datetime({ offset: true }),
      tag: z.string(),
    },
    outputSchema: { output: z.string(), success: z.boolean() },
  },
  async ({ startISO, endISO, tag }) => {
    const result = await composeAndExecuteSshCommand(
      { type: "track", args: { start: startISO, end: endISO, tag } },
      isDryRun,
    );
    let message;
    if (isDryRun) {
      message = `Dry run command: ${result.output}`;
    } else if (result.success) {
      message = `Command executed successfully: ${result.output}`;
    } else {
      message = `Command failed: ${result.output}`;
    }
    return {
      content: [{ type: "text", text: message }],
      structuredContent: { success: result.success, output: result.output },
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
