import { McpServer, Tool, Toolkit } from "@effect/ai";
import { BunSink, BunStream } from "@effect/platform-bun";
import { Effect, Layer, Logger, Schema } from "effect";

const TestPrompt = McpServer.prompt({
  name: "Test Prompt",
  description: "A test prompt to demonstrate MCP server capabilities",
  parameters: Schema.Struct({
    flightNumber: Schema.String,
  }),
  completion: {
    flightNumber: () => Effect.succeed(["FL123", "FL456", "FL789"]),
  },
  content: ({ flightNumber }) =>
    Effect.succeed(
      `Get the booking details for flight number: ${flightNumber}`,
    ),
});

const ICSTool = Tool.make("EventCreator", {
  description: "Create an ICS file with the start time and the end time",
  parameters: {
    start: Schema.Number,
    end: Schema.Number,
  },
  success: Schema.String,
}).annotate(Tool.Idempotent, true);

const ServerToolKit = Toolkit.make(ICSTool);

const TestTool = McpServer.toolkit(ServerToolKit);

const ServerToolKitLayer = ServerToolKit.toLayer({
  EventCreator: ({ start, end }) =>
    Effect.succeed(
      `This is the test for the first tool in the ICS MCP server the start was ${start} the end was ${end}!`,
    ),
});

// Merge all the resources and prompts into a single server layer
export const ServerLayer = Layer.mergeAll(
  TestPrompt,
  TestTool.pipe(Layer.provide(ServerToolKitLayer)),
).pipe(
  Layer.provide(
    McpServer.layerStdio({
      name: "ICS mcp",
      version: "1.0.0",
      stdin: BunStream.stdin,
      stdout: BunSink.stdout,
    }),
  ),
  Layer.provide(Logger.add(Logger.prettyLogger({ stderr: true }))),
);
