import { McpServer } from "@effect/ai";
import { BunSink, BunStream } from "@effect/platform-bun";
import { Effect, Layer, Logger, Schema } from "effect";
import { ICSToolImplLayer, ICSToolkitLayer } from "./Tools.js";

const TestPrompt = McpServer.prompt({
  name: "Event",
  description: "Enter an event through this template",
  parameters: Schema.Struct({
    start: Schema.String,
    end: Schema.String,
    day: Schema.String,
  }),
  completion: {
    start: () => Effect.succeed([]),
    end: () => Effect.succeed([]),
    day: () => Effect.succeed([":today", ":tomorrow", ":nextweek"]),
  },
  content: ({ start, end, day }) =>
    Effect.succeed(
      `Book an event with the start at ${start}, the end at ${end} and day ${day} use the EventCreator tool.`,
    ),
});


// Merge all the resources and prompts into a single server layer
export const ServerLayer = Layer.mergeAll(
  TestPrompt,
  ICSToolkitLayer.pipe(Layer.provide(ICSToolImplLayer)),
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
